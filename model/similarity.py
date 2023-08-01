import pandas as pd
import numpy as np
from numpy import dot
from numpy.linalg import norm

__all__ = ["Similarity"]

"""
cosine similarity version에 따라서
다른 전처리 or 후처리 모양을 가지므로
이거 정리하기
일단 cosine similarity 만드는게 우선이겠군
"""


class Cosine_similarity:
    def _cos_sin(self, A, B):
        return dot(A, B) / (norm(A) * norm(B))

    def similarity(self, df):
        similar_df = pd.DataFrame()

        for id in df.index:
            status_embedding = df["feature"][id]

            imply = pd.DataFrame()
            imply["cosine"] = df.apply(
                lambda x: self._cos_sin(x["feature"], status_embedding), axis=1
            )
            ind = imply[imply["cosine"] >= 0.8].index

            imply_df = pd.DataFrame()
            imply_df["similar_id"] = df["item_id"].iloc[ind]
            imply_df["item_id"] = df["item_id"][id]
            imply_df["item_url"] = df["file_path"][id]
            imply_df["similar_url"] = df["file_path"].iloc[ind]
            imply_df["rate"] = imply["cosine"].iloc[ind]

            similar_df = pd.concat([similar_df, imply_df])
        similar_df = similar_df.reset_index(drop=True)
        similar_df = similar_df.drop(
            similar_df[similar_df["similar_id"] == similar_df["item_id"]].index
        )

        return similar_df
