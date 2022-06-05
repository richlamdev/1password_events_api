import json
import pandas as pd

import plotly.graph_objects as go
from plotly.subplots import make_subplots


def frequency(ds, vars):
    if len(vars) > 1:
        c1 = ds[vars[0]]
        c2 = []
        for i in range(1, len(vars)):
            c2.append(ds[vars[i]])
        dfs = []
        dfs.append(
            pd.crosstab(c1, c2)
            .unstack()
            .reset_index()
            .rename(columns={0: "Count"})
        )
        dfs.append(
            pd.crosstab(c1, c2, normalize="all")
            .unstack()
            .reset_index()
            .rename(columns={0: "Percent"})
        )
        dfs = [df.set_index(vars) for df in dfs]
        df = dfs[0].join(dfs[1:]).reset_index()
        return df


def main():

    with open("item_usages.json", "r") as input_file:
        json_data = json.load(input_file)
    # print(json_data)
    df = pd.json_normalize(json_data)
    # print(df)

    # uncomment when a new csv is needed to review
    # df.to_csv("item_usages.csv")

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

    actions = df["action"].value_counts()
    operating_systems = df["client.os_name"].value_counts()
    user_name = df["user.name"].value_counts()
    vault_uuid = df["vault_uuid"].value_counts()

    reveal_action = df.loc[df["action"] == "reveal"]

    print()
    print("reveal_action:")
    print()
    print(reveal_action)
    print()
    print()

    top_vault_by_user = (
        df.groupby(["user.name", "vault_uuid"])
        .vault_uuid.value_counts()
        .nlargest(10)
    )

    # crosstab = pd.crosstab(df["vault_uuid"], df["user.name"], df["action"])

    # crosstab = frequency(df, ["vault_uuid", "user.name", "action"])

    # crosstab = crosstab_user_vault.loc[(crosstab_user_vault <= 10).any(axis=1)]

    # crosstab = crosstab.loc[:, (crosstab <= 10).any(axis=0)]

    # crosstab.to_csv("crosstab.csv")

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

    # print("actions")
    # print(actions)
    # print(actions.index[0])


#
# print()
# print("operating_systems")
# print(operating_systems)
#
# print()
# print("user_name")
# print(user_name)
#
# print()
# print("vault_uuid")
# print(vault_uuid)
#
# print("top_vault_by_user")
# print(top_vault_by_user)
# print()

# print("top_user_by_vault")
# print(top_user_by_vault)
# print()

# print("top_vault_by_os")
# print(top_vault_by_os)
# print()

# print(crosstab_user_vault.info())
# print(crosstab.info())

# print()
# print(top_vault_by_user.index[1][0])
# print()


if __name__ == "__main__":
    main()
