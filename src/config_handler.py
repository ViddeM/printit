from src.ResultWithData import ResultWithData, get_result_with_data
from src.credentials import set_password, set_cid


def set_config(config: str, cid: str) -> ResultWithData[str]:
    if config == "pass":
        set_password(cid)
    elif config == "cid":
        raise NotImplementedError(NotImplemented)

    return get_result_with_data("{0} updated successfully".format(config))
