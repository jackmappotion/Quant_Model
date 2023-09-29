class MOVING_AVERAGE_MODEL:
    def __init__(self, data) -> None:
        self.data = data

    @staticmethod
    def append_stma(data, CFG):
        """
        stma : short_term_moving_average
        """
        short_window = CFG["stma_window"]
        data["STMA"] = data["Value"].rolling(window=short_window).mean()
        return data

    @staticmethod
    def append_ltma(data, CFG):
        """
        ltma : long_term_moving_average
        """
        long_window = CFG["ltma_window"]
        data["LTMA"] = data["Value"].rolling(window=long_window).mean()
        return data

    @staticmethod
    def append_signal(data):
        """
        Signal : {1:매수, -1:매도}
        """
        data["Signal"] = 0
        data.loc[data["STMA"] > data["LTMA"], "Signal"] = 1
        data.loc[data["STMA"] < data["LTMA"], "Signal"] = -1
        return data

    def __call__(self, CFG):
        data = self.data

        data = self.append_stma(data, CFG)
        data = self.append_ltma(data, CFG)
        data = self.append_signal(data)

        return data
