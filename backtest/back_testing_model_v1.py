class BACK_TESTING_MODEL:
    def __init__(self, result_df, init_cash) -> None:
        self.result_df = result_df
        self.init_cash = init_cash

    @staticmethod
    def calculate_daily_cash(current_cash, percentage=0.5):
        daily_cash = current_cash * percentage
        return daily_cash

    @staticmethod
    def calculate_buying_order(price, daily_cash):
        buying_order = daily_cash // price
        return buying_order

    @staticmethod
    def calculate_buying_cash(buying_order, price):
        buying_cash = buying_order * price
        return buying_cash

    @staticmethod
    def calculate_selling_order(total_position, percentage=0.5):
        selling_order = int(total_position * percentage)
        return selling_order

    @staticmethod
    def calculate_selling_cash(selling_order, price):
        selling_cash = selling_order * price
        return selling_cash

    def __call__(self):
        result_df = self.result_df
        init_cash = self.init_cash

        equity_hist = list()
        current_cash = init_cash
        total_position = 0

        for index, row in result_df.iterrows():
            price = row["Price"]
            signal = row["Signal"]
            daily_cash = self.calculate_daily_cash(current_cash)
            if signal == 1:
                buying_order = self.calculate_buying_order(price, daily_cash)
                total_position += buying_order

                buying_cash = self.calculate_buying_cash(buying_order, price)
                current_cash -= buying_cash

            elif signal == -1:
                selling_order = self.calculate_selling_order(total_position)
                total_position -= selling_order

                selling_cash = self.calculate_selling_cash(selling_order, price)
                current_cash += selling_cash

            equity_hist.append(total_position * price + current_cash)
        return equity_hist

"""
back_testing_model = BACK_TESTING_MODEL(bbm_result_df, 100_000_000)
equity_hist = back_testing_model()
"""
