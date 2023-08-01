from model.embedding import FeatureExtractor
from model.similarity import Similarity

import pandas as pd

import settings


class Model:
    def __init__(self):
        self.item_id = settings.item_id
        self.similar_id = settings.similar_id
        self.file_path = settings.file_path
        self.similarity = Similarity()

    def _apply_embedding(
        self, df, col_name: str = "url", embedding_col_name: str = "feature"
    ):
        fe = FeatureExtractor()
        df[embedding_col_name] = df[col_name].apply(lambda x: fe.get_feature(x))

        return df

    def _apply_similarity(
        self, df, apply_col: str = "feature", similar_limit: float = 0.8
    ):
        """
        알아서 정리하고 코드 수정해라
        귀찮다
        """
        similar_df = pd.DataFrame()

        for id in df.index:
            status_embedding = df[apply_col][id]

            imply = pd.DataFrame()

            imply["similarity"] = df.apply(
                lambda x: self.similarity.cos_sin(x[apply_col], status_embedding),
                axis=1,
            )
            ind = imply[imply["similarity"] >= similar_limit].index

            imply_df = pd.DataFrame()
            imply_df[self.similar_id] = df[self.item_id].iloc[ind]
            imply_df[self.item_id] = df[self.item_id][id]
            imply_df["similar_url"] = df[self.file_path].iloc[ind]
            imply_df["item_url"] = df[self.file_path][id]
            imply_df["rate"] = imply["similarity"].iloc[ind]

            similar_df = pd.concat([similar_df, imply_df])

        similar_df = similar_df.reset_index(drop=True)
        similar_df = similar_df.drop(
            similar_df[similar_df[self.similar_id] == similar_df[self.item_id]].index
        )

        return similar_df
