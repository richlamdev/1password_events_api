import json
import pandas as pd

import plotly.graph_objects as go
from plotly.subplots import make_subplots


def main():

    with open("item_usages.json", "r") as input_file:
        json_data = json.load(input_file)
    # print(json_data)
    df = pd.json_normalize(json_data)
    # print(df)

    df.drop(
        [
            "uuid",
            "used_version",
            "user.uuid",
            "user.email",
            "client.app_name",
            "client.app_version",
            "client.platform_name",
            "client.platform_version",
            "client.os_version",
            "location.latitude",
            "location.longitude",
        ],
        axis=1,
        inplace=True,
    )

    df.to_csv("item_usages_new.csv")
    # print(df)

    # uncomment when a new csv is needed to review
    df.to_csv("item_usages.csv")

    actions = df["action"].value_counts()
    operating_systems = df["client.os_name"].value_counts()
    user_name = df["user.name"].value_counts()
    vault_uuid = df["vault_uuid"].value_counts()

    reveal_action = df.loc[df["action"] == "reveal"]

    top_vault_by_user = (
        df.groupby(["user.name", "vault_uuid"])
        .vault_uuid.value_counts()
        .nlargest(10)
    )

    crosstab_user_vault = pd.crosstab(df["vault_uuid"], df["user.name"])

    crosstab = crosstab_user_vault.loc[(crosstab_user_vault <= 10).any(axis=1)]

    crosstab = crosstab_user_vault.loc[
        :, (crosstab_user_vault <= 10).any(axis=0)
    ]

    crosstab.to_csv("crosstab.csv")

    top_user_by_vault = (
        df.groupby(["vault_uuid", "user.name"])
        .vault_uuid.value_counts()
        .nlargest(10)
    )

    top_vault_by_os = (
        df.groupby(["client.os_name", "vault_uuid"])
        .vault_uuid.value_counts()
        .nlargest(10)
    )

    print("actions")
    print(actions)
    print(actions.index[0])

    ## Start common graph setup ##
    fig = make_subplots(
        rows=2,
        cols=1,
        horizontal_spacing=0.9,
        vertical_spacing=0.1,
        specs=[[{"type": "scatter"}], [{"type": "table"}]],
        subplot_titles=("Actions", "Reveal Actions", ""),
    )
    # End common graph setup  ##

    for action in range(len(actions)):
        fig.add_trace(
            go.Bar(
                y=[actions[action]],
                hovertemplate=(
                    actions.index[action] + ": %{y}" + "<extra></extra>"
                ),
                x=[actions.index[action]],
            ),
            row=1,
            col=1,
        )

    # print(reveal_action)

    fig.add_trace(
        go.Table(
            columnwidth=[300, 300, 300, 100, 150, 175, 400, 200, 200, 150],
            header=dict(
                values=list(reveal_action.columns),
                line_color="darkslategray",
                fill_color="royalblue",
                align="center",
                font=dict(color="white", size=16),
                height=50,
            ),
            cells=dict(
                values=reveal_action.transpose().values.tolist(),
                line_color="darkslategray",
                fill=dict(color=["paleturquoise", "white"]),
                align="center",
                font_size=14,
                height=40,
                # width=100,
            ),
        ),
        row=2,
        col=1,
    )

    # fig.add_trace(reveal_action_table, row=2, col=1)

    # fig = go.Figure(
    # data=[
    # go.Table(
    # header=dict(values=list(reveal_action.columns)),
    # cells=dict(values=reveal_action.transpose().values.tolist()),
    # )
    # ]
    # )
    fig.update_layout(autosize=True)

    fig.show()


if __name__ == "__main__":
    main()
