# Rec-homeShopping
## CTR Predict
사용자가 바로 다음에 볼 상품을 예측하는 추천모델 개발

## Ensemble Ranking Prediction Model


```
dataset    #개별표기 생략
	ㄴ original json data 
	ㄴ train - valid - test split data
	ㄴ train - test submission 

notebook    #train 과정
	ㄴ 1.jsonToDataFrame.ipynb
	ㄴ 2.eda.ipynb
	ㄴ 3.featureExtract.ipynb
	ㄴ 4.splitTrainData.ipynb
	ㄴ 5.MostPopular.ipynb
	ㄴ 6.ALS.ipynb
	ㄴ 7.Apriori.ipynb 
	ㄴ 8.LgbmRanker.ipynb
	ㄴ 9.ensemble.ipynb
	ㄴ 10.word2vec-segmentation.ipynb
	ㄴ 10.word2vec.ipynb
	ㄴ 11.BidirectionalLSTM.ipynb

output      #개별표기 생략
	ㄴ candidate, feature 
	ㄴ model.pkl

src   #여러 번 사용되는 코드.py화
	ㄴ candidates.py
	ㄴ dataLoad.py
	ㄴ featureEngineering.py
	ㄴ metric.py

submission  #최종제출 모델 파일
	ㄴ final-als.ipynb
	ㄴ final-ensemble.ipynb  
	ㄴ final-ensemble2.ipynb  #OOM issue 대안책
```

    
Rule Based, CF, Boosting, NLP 기반 모델 등 다양한 모델을 학습하고, 그로부터 얻어낼 수 있는 다양한 Feature/Candidate/information을 활용해 LgbmRanker 모델의 성능을 극대화합니다.
    
딥러닝 모델에 비해 학습 속도가 빠르며, 다양한 타입의 모델을 사용해 보며 데이터셋에 어떤 타입의 모델이 더 효과적인지 파악할 수 있습니다.    
    


## Rule Based Model :
**Most Popular**     
ㄴ general_most_popular : 데이터셋의 마지막 n주, 마지막 n-1주의 인기상품을 찾아냅니다.    
ㄴ recent30days_MP : 데이터셋의  마지막 n0일(default = 30)간의 인기상품을 찾아냅니다.    

**Apriori**    
ㄴ 연관 규칙을 활용해 한 아이템과 함께 조회되는 빈도가 높은 아이템을 찾아냅니다.

## Content Based Model :
**ALS (matrix factorization)**    
ㄴ 행렬 분해를 통해, user-item 사이의 잠재선호도를 찾아냅니다. 학습 결과를 출력할 때에는, 중복추천을 허용했습니다.    

## Boosting :
**LgbmRanker**    
ㄴ 강력한 성능을 가진 Boosting 모델을 통해, 앙상블을 구축합니다. 다른 모델들의 결과물들을 적용합니다. 학습결과는 아이템에 대한 유저의 선호확률이며, 이를 top 10 Ranking합니다.    
train dataset을 학습했던 모델을 저장해 test 학습에 재사용합니다.    

## NLP :
**Word2Vec**     
ㄴ 유저의 마지막 조회 아이템을 매개로, 해당 아이템과 연관도가 높은 아이템을 찾아냅니다.    
ㄴ 아이템 이름을 통해 item segmentation (clustering)을 합니다.    