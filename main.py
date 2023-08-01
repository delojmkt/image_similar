import os
import warnings

warnings.filterwarnings(action="ignore")

from model import FeatureExtractor

import pandas as pd

from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument("-f", "--file_path", type=str)

args = parser.parse_args()

if __name__ == "__main__":
    FLAGS = args

    file_path = FLAGS.file_path if FLAGS.file_path else "data.csv"

    # 01. loading data
    df = pd.read_csv(file_path)

    # 02. preprocess data
    fe = FeatureExtractor()

    df["feature"] = df["file_path"].apply(lambda x: fe.get_feature(x))

    similar_df = pd.DataFrame()

    for id in df.index:
        status_embedding = df["feature"][id]

        imply_1 = pd.DataFrame()

        imply_1["cosine"] = df.apply(
            lambda x: cos_sim(x["feature"], status_embedding), axis=1
        )
        ind = imply_1[imply_1["cosine"] >= 0.8].index

        imply_df = pd.DataFrame()
        imply_df["similar_id"] = df["item_id"].iloc[ind]
        imply_df["item_id"] = df["item_id"][id]
        imply_df["item_url"] = df["file_path"][id]
        imply_df["similar_url"] = df["file_path"].iloc[ind]
        imply_df["rate"] = imply_1["cosine"].iloc[ind]

        similar_df = pd.concat([similar_df, imply_df])

    similar_df = similar_df.reset_index(drop=True)
    similar_df = similar_df.drop(
        similar_df[similar_df["similar_id"] == similar_df["item_id"]].index
    )

    # 최적화 하기 귀찮다
    # 알아서 미래의 내가 해주겠지
