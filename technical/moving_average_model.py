class MOVING_AVERAGE_MODEL:
    """
    Price
    """
    def __init__(self, data) -> None:
        self.data = data

    @staticmethod
    def append_stma(data, CFG):
        """
        STMA : short_term_moving_average
        """
        short_window = CFG["stma_window"]
        data["STMA"] = data["Price"].rolling(window=short_window).mean()
        return data

    @staticmethod
    def append_ltma(data, CFG):
        """
        LTMA : long_term_moving_average
        """
        long_window = CFG["ltma_window"]
        data["LTMA"] = data["Price"].rolling(window=long_window).mean()
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
