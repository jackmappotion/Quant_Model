class STOCHASTIC_OSCILLATOR_MODEL:
    def __init__(self, data) -> None:
        self.data = data

    @staticmethod
    def append_lowestlow(data, window=14):
        data["LowestLow"] = data["Value"].rolling(window=window).min()
        return data

    @staticmethod
    def append_highesthigh(data, window=14):
        data["HighestHigh"] = data["Value"].rolling(window=window).max()
        return data

    @staticmethod
    def append_fso(data):
        """
        FSO : Fast Stochastic Oscillator
        """
        data["FSO"] = (
            (data["Value"] - data["LowestLow"])
            / (data["HighestHigh"] - data["LowestLow"])
        ) * 100
        return data

    @staticmethod
    def append_sso(data, window=3):
        """
        SSO : Slow Stochastic Oscillator
        """
        data["SSO"] = data["FSO"].rolling(window=window).mean()
        return data

    @staticmethod
    def append_signal(data):
        data["Signal"] = 0
        data.loc[(data["FSO"] < data["SSO"]) & (data["FSO"] < 20), "Signal"] = 0.5
        data.loc[(data["FSO"] > data["SSO"]) & (data["FSO"] < 20), "Signal"] = 1

        data.loc[(data["FSO"] > data["SSO"]) & (data["FSO"] > 80), "Signal"] = -0.5
        data.loc[(data["FSO"] < data["SSO"]) & (data["FSO"] > 20), "Signal"] = -1
        return data

    def __call__(self):
        data = self.data

        data = self.append_lowestlow(data)
        data = self.append_highesthigh(data)

        data = self.append_fso(data)
        data = self.append_sso(data)
        data = self.append_signal(data)
        return data
