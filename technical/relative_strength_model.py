class RELATIVE_STRENGTH_MODEL:
    def __init__(self, data) -> None:
        self.data = data

    @staticmethod
    def append_diff(data):
        """
        Diff : Value Difference
        """
        data["Diff"] = data["Price"].diff(periods=1)
        return data

    @staticmethod
    def append_gain(data):
        data["Gain"] = data["Diff"].apply(lambda x: x if x > 0 else 0)
        return data

    @staticmethod
    def append_mgain(data, CFG):
        """
        MGain : Mean Gain
        """
        window = CFG["ma_window"]
        data["MGain"] = data["Gain"].rolling(window=window).mean()
        return data

    @staticmethod
    def append_loss(data):
        data["Loss"] = data["Diff"].apply(lambda x: -x if x < 0 else 0)
        return data

    @staticmethod
    def append_mloss(data, CFG):
        """
        MLoss : Mean Loss
        """
        window = CFG["ma_window"]
        data["MLoss"] = data["Loss"].rolling(window=window).mean()
        return data

    @staticmethod
    def append_rs(data):
        """
        RS : Relative Strength
        """
        data["RS"] = data["MGain"] / data["MLoss"]
        return data

    @staticmethod
    def append_rsi(data):
        """
        RSI : Relative Strength Index
        """
        data["RSI"] = 100 - (100 / (1 + data["RS"]))
        return data

    @staticmethod
    def append_signal(data):
        """
        signal : {1:매수, -1:매도}
        """
        data["Signal"] = 0
        data.loc[data["RSI"] < 30, "Signal"] = 1
        data.loc[data["RSI"] > 70, "Signal"] = -1
        return data

    def __call__(self, CFG):
        data = self.data

        data = self.append_diff(data)

        data = self.append_gain(data)
        data = self.append_mgain(data, CFG)

        data = self.append_loss(data)
        data = self.append_mloss(data, CFG)

        data = self.append_rs(data)
        data = self.append_rsi(data)
        data = self.append_signal(data)
        return data
