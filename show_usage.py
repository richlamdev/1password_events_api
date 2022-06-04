import json
import pandas as pd

# import dash
# import dash_core_components as dcc
# import dash_html_components as html
# import dateutil.parser

import plotly.graph_objects as go
from plotly.subplots import make_subplots


def main():

    with open("item_usages.json", "r") as input_file:
        json_data = json.load(input_file)
    # print(json_data)
    df = pd.json_normalize(json_data)
    # print(df)
    df.to_csv("item_usages.csv")

    actions = df["action"].value_counts()
    operating_systems = df["client.os_name"].value_counts()
    user_name = df["user.name"].value_counts()
    vault_uuid = df["vault_uuid"].value_counts()

    top_vault_by_user = (
        df.groupby(["user.name", "vault_uuid"])
        .vault_uuid.value_counts()
        .nlargest(10)
    )

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
    print(actions.reveal)
    # print(actions[""]) #for null value

    print()
    print("operating_systems")
    print(operating_systems)

    print()
    print("user_name")
    print(user_name)

    print()
    print("vault_uuid")
    print(vault_uuid)

    print("top_vault_by_user")
    print(top_vault_by_user)
    print()

    print("top_user_by_vault")
    print(top_user_by_vault)
    print()

    print("top_vault_by_os")
    print(top_vault_by_os)
    print()

    ## Start common graph setup ##
    fig = make_subplots(
        rows=3,
        cols=2,
        # horizontal_spacing=0.10,
        # vertical_spacing=0.06,
        # specs=[
        # [{"type": "scatter", "colspan": 2}, None],
        # [{"type": "table", "colspan": 1}, None],
        # [{"type": "scatter", "colspan": 2}, None],
        # ],
        subplot_titles=("Actions", "", ""),
    )
    ## End common graph setup  ##

    fig.add_trace(
        go.Bar(
            y=[actions["fill"]],
            hovertemplate=("fill: %{y}" + "<extra></extra>"),
            x=["fill"],
        ),
        row=1,
        col=1,
    )

    fig.add_trace(
        go.Bar(
            y=[actions["server-fetch"]],
            hovertemplate=("server-fetch: %{y}" + "<extra></extra>"),
            x=["server-fetch"],
        ),
        row=1,
        col=1,
    )

    fig.add_trace(
        go.Bar(
            y=[actions[""]],
            hovertemplate=("null: %{y}" + "<extra></extra>"),
            x=["null"],
        ),
        row=1,
        col=1,
    )

    fig.add_trace(
        go.Bar(
            y=[actions["secure-copy"]],
            hovertemplate=("secure-copy: %{y}" + "<extra></extra>"),
            x=["secure-copy"],
        ),
        row=1,
        col=1,
    )

    fig.add_trace(
        go.Bar(
            y=[actions["server-update"]],
            hovertemplate=("server-update: %{y}" + "<extra></extra>"),
            x=["secure-update"],
        ),
        row=1,
        col=1,
    )

    fig.add_trace(
        go.Bar(
            y=[actions["server-create"]],
            hovertemplate=("server-create: %{y}" + "<extra></extra>"),
            x=["secure-create"],
        ),
        row=1,
        col=1,
    )

    fig.add_trace(
        go.Bar(
            y=[actions["reveal"]],
            hovertemplate=("server-reveal: %{y}" + "<extra></extra>"),
            x=["secure-reveal"],
        ),
        row=1,
        col=1,
    )

    fig.show()


if __name__ == "__main__":
    main()
