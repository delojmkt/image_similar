import requests

__all__ = ["get_query"]


def get_query():
    return """
                SELECT
                ti.item_id,
                A.basegrade_cd,
                tfi.file_path 
                FROM monhangdb.tb_item ti
                LEFT JOIN monhangdb.tb_item_image_mapper tiim ON ti.item_id = tiim.item_id 
                LEFT JOIN monhangdb.tb_file_image tfi ON tiim.file_image_id = tfi.file_image_id 
                INNER JOIN (SELECT 
                    tpim.item_id 
                    , ts.f_basegrade_cd AS basegrade_cd 
                FROM monhangdb.tb_passage_item_mapper tpim 
                LEFT JOIN monhangdb.tb_passage tp ON tpim.passage_id = tp.passage_id 
                LEFT JOIN monhangdb.tb_subject ts ON tp.subject_id = ts.f_subject_id 
                WHERE 1=1
                AND ts.f_area_cd IN ('MA','HM')
                AND ts.f_emh_cd = 'E0' -- ('E0','M0','H0')
                ) A ON ti.item_id = A.item_id 
                WHERE 1=1
                AND tfi.file_path IS NOT NULL
                LIMIT 1000
                ;
            """
