#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
https://www.iwencai.com/unifiedwap/home/index
"""
import pandas as pd
import requests


# pip install tqdm
# pip install requests
# pip install pandas

def get_tqdm(enable: bool = True):
    # 显示进度条
    if not enable:
        # 如果进度条被禁用，返回一个不显示进度条的 tqdm 对象
        return lambda iterable, *args, **kwargs: iterable
    try:
        # 尝试检查是否在 jupyter notebook 环境中，有利于退出进度条
        # noinspection PyUnresolvedReferences
        shell = get_ipython().__class__.__name__
        if shell == "ZMQInteractiveShell":
            from tqdm.notebook import tqdm
        else:
            from tqdm import tqdm
    except (NameError, ImportError):
        # 如果不在 Jupyter 环境中，就使用标准 tqdm
        from tqdm import tqdm

    return tqdm


def get_wc_data(query: str = "今日涨停", pages: int = 1) -> pd.DataFrame:
    """
    问财
    https://www.iwencai.com/unifiedwap/result
    """
    url = "https://www.iwencai.com/gateway/urp/v7/landing/getDataList"
    params = {
        "query": query,
        "urp_sort_way": "desc",
        "urp_sort_index": "",
        "page": "1",
        "perpage": "100",
        "addheaderindexes": "",
        "condition": '',
        "codelist": "",
        "indexnamelimit": "",
        "ret": "json_all",
        "source": "Ths_iwencai_Xuangu",
        "urp_use_sort": "1",
        "uuids[0]": "24087",
        "query_type": "stock",
        "comp_id": "6836372",
        "business_cat": "soniu",
        "uuid": "24087",
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    }
    big_df = pd.DataFrame()
    tqdm = get_tqdm()
    for page in tqdm(range(1, pages + 1), leave=False):
        params.update(
            {
                "page": page,
            }
        )
        r = requests.get(url, params=params, headers=headers)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json["answer"]["components"][0]["data"]["datas"])
        big_df = pd.concat([big_df, temp_df], ignore_index=True)
    big_df.reset_index(inplace=True)
    return big_df


if __name__ == "__main__":
    page = 3  # 取前几页的数据
    querys = "今日热度前250" # 问句
    data = get_wc_data(query=querys, pages=page)
    print(data)
