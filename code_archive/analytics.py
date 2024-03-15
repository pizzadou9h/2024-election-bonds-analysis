import pandas as pd
import plotly.express as px

class PoliticalFundingAnalyzer:
    def __init__(self):
        self.e_bonds_party_df = pd.read_csv("e-bonds_party.csv")
        self.matched_transactions_df = pd.read_csv("matched_transactions.csv")
        self.e_bonds_company_df = pd.read_csv("e-bonds_company.csv")

    def party_funds_distribution(self):
        party_funds = self.matched_transactions_df.groupby("Political Party")["Amount"].sum() / 1000000000
        party_funds_top7 = party_funds.nlargest(7)
        party_funds_others = party_funds.sum() - party_funds_top7.sum()
        party_funds_top7["Others"] = party_funds_others
        fig = px.pie(party_funds_top7, values=party_funds_top7, names=party_funds_top7.index, title="Distribution of Funds Received by Political Parties")
        fig.update_traces(textinfo='percent+label', texttemplate='%{label}: %{percent}')
        fig.update_layout(width=800, height=600)  # Increase the size of the chart
        px.plotly_chart(fig)

    def top_purchasers(self):
        purchaser_funds = self.matched_transactions_df.groupby("Purchaser Name")["Amount"].sum()
        purchaser_funds_top10 = purchaser_funds.nlargest(10)
        purchaser_funds_others = purchaser_funds.sum() - purchaser_funds_top10.sum()
        purchaser_funds_top10["Others"] = purchaser_funds_others
        fig = px.pie(purchaser_funds_top10, values=purchaser_funds_top10, names=purchaser_funds_top10.index, title="Top Purchasers")
        fig.update_layout(width=800, height=600)  # Increase the size of the chart
        px.plotly_chart(fig)

    def bjp_donations(self):
        bjp_donations = self.matched_transactions_df[self.matched_transactions_df["Political Party"] == "BHARTIYA JANTA PARTY"].groupby("Purchaser Name")["Amount"].sum().reset_index().sort_values(by="Amount", ascending=False)
        bjp_donations["Amount"] = (bjp_donations["Amount"]/1000000).apply(lambda x: "{:,}".format(x))
        bjp_donations["Amount"] =  " INR " + bjp_donations["Amount"] + " M"
        button_key = "bjp_donations_download"  # Unique key for the button
        button = px.button("Download Excel", key=button_key)
        if button:
            bjp_donations.to_excel("bjp_donations.xlsx", index=False)
            px.success("Excel file downloaded successfully!")
        px.table(bjp_donations)

    def congress_donations(self):
        
        congress_donations = self.matched_transactions_df[self.matched_transactions_df["Political Party"] == "PRESIDENT, ALL INDIA CONGRESS COMMITTEE"].groupby("Purchaser Name")["Amount"].sum().reset_index().sort_values(by="Amount", ascending=False)
        congress_donations["Amount"] = (congress_donations["Amount"]/1000000).apply(lambda x: "{:,}".format(x))
        congress_donations["Amount"] =  " INR " + congress_donations["Amount"] + " M"
        button_key = "congress_donations_download"  # Unique key for the button
        button = px.button("Download Excel", key=button_key)
        if button:
            congress_donations.to_excel("congress_donations.xlsx", index=False)
            px.success("Excel file downloaded successfully!", icon="🎉")
        px.table(congress_donations)

def main():
    analyzer = PoliticalFundingAnalyzer()
    analyzer.top_purchasers()


if __name__ == "__main__":
    main()