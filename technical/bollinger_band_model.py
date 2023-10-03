class BOLLINGER_BAND_MODEL:
    def __init__(self, data) -> None:
        self.data = data

    @staticmethod
    def append_ma(data, CFG):
        """
        MA : moving_average
        """
        window = CFG["ma_window"]
        data["MA"] = data["Price"].rolling(window=window).mean()
        return data

    @staticmethod
    def append_std(data, CFG):
        """
        STD : moving_average_std
        """
        window = CFG["ma_window"]
        data["STD"] = data["Price"].rolling(window=window).std()
        return data

    @staticmethod
    def append_lowerband(data, CFG):
        """
        LowerBand : lower_band
        """
        std_coef = CFG["std_coef"]
        data["LowerBand"] = data["MA"] - std_coef * data["STD"]
        return data

    @staticmethod
    def append_upperband(data, CFG):
        """
        UpperBand : upper_band
        """
        std_coef = CFG["std_coef"]
        data["UpperBand"] = data["MA"] + std_coef * data["STD"]
        return data

    @staticmethod
    def append_signal(data):
        """
        Signal : {1:매수, -1:매도}
        """
        data["Signal"] = 0
        data.loc[data["Price"] > data["UpperBand"], "Signal"] = -1
        data.loc[data["Price"] < data["LowerBand"], "Signal"] = 1
        return data

    def __call__(self, CFG):
        data = self.data

        data = self.append_ma(data, CFG)
        data = self.append_std(data, CFG)
        data = self.append_lowerband(data, CFG)
        data = self.append_upperband(data, CFG)
        
        data = self.append_signal(data)

        return data
    
