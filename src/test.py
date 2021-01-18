import pandas as pd

import numpy as np





if __name__ == '__main__':
	humans_df=pd.read_csv('data/humans.csv')
	for Col,Header in zip(humans_df.sum(),humans_df.columns):
		print(len(Col)/humans_df[[Header]].dropna().shape[0])
