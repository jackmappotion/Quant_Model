from typing import Any


class MONEY_FLOW_MODEL:
    def __init__(self, data) -> None:
        self.data = data

    @staticmethod
    def append_pmf(data):
        """
        PMF : Positive Money Flow
        """
        data["PMF"] = (data["Price"].diff() > 0) * data["Price"] * data["Volume"]
        return data

    @staticmethod
    def append_pmfr(data, window):
        """
        PMFR : Positive Money Flow Ratio
        """
        data["PMFR"] = (
            data["PMF"].rolling(window=window).sum()
            / data["NMF"].rolling(window=window).sum()
        )
        return data

    @staticmethod
    def append_nmf(data):
        """
        NMF : Negative Money Flow
        """
        data["NMF"] = (data["Price"].diff() < 0) * data["Price"] * data["Volume"]
        return data

    @staticmethod
    def append_nmfr(data):
        """
        NMFR : Negative Money Flow Ratio
        """
        data["NMFR"] = 1 / data["PMFR"]
        return data

    @staticmethod
    def append_mfi(data):
        """
        MFI : Money Flow Index
        """
        data["MFI"] = 100 - (100 / (1 + data["PMFR"] / data["NMFR"]))
        return data

    @staticmethod
    def append_signal(data):
        """
        Signal : {1:매수, -1:매도}
        """
        data["Signal"] = 0
        data.loc[data["MFI"] < 30, "Signal"] = 1
        data.loc[data["MFI"] > 70, "Signal"] = -1
        return data

    def __call__(self, CFG):
        data = self.data

        data = self.append_pmf(data)
        data = self.append_nmf(data)

        data = self.append_pmfr(data, CFG["window"])
        data = self.append_nmfr(data)

        data = self.append_mfi(data)

        data = self.append_signal(data)
        return data
