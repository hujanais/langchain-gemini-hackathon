import pandas as pd

class FiassUtility():        

    def store_to_df(self, store):
        v_dict = store.docstore._dict
        data_rows = []
        for k in v_dict.keys():
            print(v_dict[k])
            print()
        #     doc_name = v_dict[k].metadata['source'].split('/')[-1]
        #     page_number = v_dict[k].metadata['page']+1
        #     content = v_dict[k].page_content
        #     data_rows.append({"chunk_id":k, "document":doc_name, "page":page_number, "content":content})
        # vector_df = pd.DataFrame(data_rows)
        # return vector_df
