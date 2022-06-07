import json
import pandas as pd

import plotly.graph_objects as go
from plotly.subplots import make_subplots


def main():

    with open("item_usages.json", "r") as input_file:
        json_data = json.load(input_file)
    # print(json_data)

    # flatten the json data
    df = pd.json_normalize(json_data)
    # uncomment to generate a new csv, if needed to review via excel
    # df.to_csv("item_usages_full.csv")

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

    # uncomment when a new csv is needed to review
    # df.to_csv("item_usages_modified.csv")
    # print(df)

    # replace blank cells in action column with "null"
    df["action"].replace({"": "null"}, inplace=True)

    actions = df["action"].value_counts()
    reveal_action = df.loc[df["action"] == "reveal"]
    # print("actions")
    # print(actions)
    # print(actions.index[0])

    linux = df.loc[df["client.os_name"] == "Linux"]

    top_item_by_user = (
        df.groupby(["item_uuid", "user.name"])
        .size()
        .nlargest(15)
        .reset_index(name="count")
    )
    # convert pandas series to dataframe to easily display in a Table
    top_item_by_user = pd.DataFrame(top_item_by_user)
    # write to file to view with excel
    # top_item_by_user.to_csv("top_item_by_user.csv")

    windows = df.loc[df["client.os_name"] == "Windows"]

    windows_users_groupby_vault = (
        windows.groupby(["vault_uuid", "user.name"])
        .size()
        # .nlargest(15)
        .reset_index(name="count")
        .sort_values(["count"], ascending=False)
        .drop_duplicates(subset=["vault_uuid"])
        # .tail(75)
        # .head(30)
    )

    print()
    print("windows_user_groupby_vault:")
    print(windows_users_groupby_vault)
    print()

    # windows_users_groupby_vault.to_csv("windows_users_vault.csv")

    ## Start common graph setup ##
    fig = make_subplots(
        rows=5,
        cols=1,
        horizontal_spacing=0.5,
        vertical_spacing=0.1,
        specs=[
            [{"type": "bar"}],
            [{"type": "table"}],
            [{"type": "table"}],
            [{"type": "table"}],
            [{"type": "table"}],
        ],
        subplot_titles=(
            "Actions",
            "Reveal Actions",
            "Non-Windows/MacOS/Android OS",
            "Top Item Usage",
            "Top Vault Usage - Windows only",
        ),
    )

    # adjust title font size
    fig.update_annotations(font_size=20)
    # End common graph setup  ##

    for action in range(len(actions)):
        fig.add_trace(
            go.Bar(
                name=actions.index[action],
                y=[actions[action]],
                hovertemplate=(
                    actions.index[action] + ": %{y}" + "<extra></extra>"
                ),
                x=[actions.index[action]],
            ),
            row=1,
            col=1,
        )

    fig.update_layout(
        yaxis=dict(
            title="Number of actions", titlefont_size=16, tickfont_size=14
        ),
        xaxis_tickfont_size=14,
        legend=dict(
            bgcolor="rgba(255,255,255,0)", bordercolor="rgba(255,255,255,0)"
        ),
    )

    fig.add_trace(
        go.Table(
            columnwidth=[400, 400, 300, 100, 150, 175, 400, 200, 200, 150],
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
            ),
        ),
        row=2,
        col=1,
    )

    fig.add_trace(
        go.Table(
            columnwidth=[400, 400, 300, 100, 150, 175, 400, 200, 200, 150],
            header=dict(
                values=list(linux.columns),
                line_color="darkslategray",
                fill_color="royalblue",
                align="center",
                font=dict(color="white", size=16),
                height=50,
            ),
            cells=dict(
                values=linux.transpose().values.tolist(),
                line_color="darkslategray",
                fill=dict(color=["paleturquoise", "white"]),
                align="center",
                font_size=14,
                height=40,
            ),
        ),
        row=3,
        col=1,
    )

    fig.add_trace(
        go.Table(
            columnwidth=[400, 400, 300],
            header=dict(
                values=list(top_item_by_user.columns),
                # values=["item", "test", "test"],
                line_color="darkslategray",
                fill_color="royalblue",
                align="center",
                font=dict(color="white", size=16),
                height=50,
            ),
            cells=dict(
                values=top_item_by_user.transpose().values.tolist(),
                line_color="darkslategray",
                fill=dict(color=["paleturquoise", "white"]),
                align="center",
                font_size=14,
                height=40,
            ),
        ),
        row=4,
        col=1,
    )

    fig.add_trace(
        go.Table(
            columnwidth=[400, 400, 300],
            header=dict(
                values=list(windows_users_groupby_vault.columns),
                # values=["item", "test", "test"],
                line_color="darkslategray",
                fill_color="royalblue",
                align="center",
                font=dict(color="white", size=16),
                height=50,
            ),
            cells=dict(
                values=windows_users_groupby_vault.transpose().values.tolist(),
                line_color="darkslategray",
                fill=dict(color=["paleturquoise", "white"]),
                align="center",
                font_size=14,
                height=40,
            ),
        ),
        row=5,
        col=1,
    )

    # windows_users_groupby_vault
    fig.update_layout(autosize=True, height=2500, showlegend=True)

    fig.show()


if __name__ == "__main__":
    main()
