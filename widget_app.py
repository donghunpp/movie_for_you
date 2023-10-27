import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from gensim.models import Word2Vec
from scipy.io import mmread
import pickle
from PyQt5.QtCore import QStringListModel

form_window = uic.loadUiType('./movie_recommendation.ui')[0]
class Exam(QWidget, form_window):           ## 상속해서 다 가지게 된다. # 클래스를 만든 것
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.Tfidf_matrix = mmread('./models/Tfidf_movie_review.mtx').tocsr()
        with open('./models/tfidf.pickle', 'rb') as f:
            self.Tfidf = pickle.load(f)
        self.embedding_model = Word2Vec.load('./models/word2vec_movie_review.model')

        self.df_reviews = pd.read_csv('./crawling_data/cleaned_one_review.csv')
        self.titles = list(self.df_reviews['titles'])
        self.titles.sort()
        for title in self.titles:
            self.comboBox.addItem(title)
        self.comboBox.currentIndexChanged.connect(self.combobox_slot)  #클릭되면 실행

    def combobox_slot(self):                               #
        title = self.comboBox.currentText()
        recommendation = self.recommendation_by_movie_title(title)
        self.lbl_recommendation.setText(recommendation)

    def recommendation_by_movie_title(self, title):         # 인덱스 받아옴
        movie_idx = self.df_reviews[self.df_reviews['titles'] == title].index[0]
        cosine_sim = linear_kernel(self.Tfidf_matrix[movie_idx], self.Tfidf_matrix)
        recommendation = self.getRecommendation(cosine_sim)
        return recommendation

    def getRecommendation(self, cosine_sim):        # 유사한 영화 0~10번까지 11개 찾아서 줌
        simScore = list(enumerate(cosine_sim[-1]))
        simScore = sorted(simScore, key = lambda x:x[1], reverse = True)
        simScore = simScore[:11]
        moviIdx = [i[0] for i in simScore]
        recMovieList = self.df_reviews.iloc[moviIdx, 0]
        recMovieList = '\n'.join(recMovieList[1:])          # 줄 바꿈으로 띄어쓰기
        print(recMovieList)
        return recMovieList

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = Exam()
    mainWindow.show()
    sys.exit(app.exec_())           ## 윈도우를 계속 유지시켜주는 함수
