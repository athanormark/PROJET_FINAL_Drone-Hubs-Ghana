"""Page d'analyse ML du reseau MASA."""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from app.config import OPERATOR_COLORS

_DARK_LAYOUT: dict = {
    "paper_bgcolor": "#0A1628",
    "plot_bgcolor": "#0F1D2E",
    "font": {
        "color": "#E8EDF2",
        "family": "Inter, sans-serif",
    },
    "xaxis": {
        "gridcolor": "rgba(136,153,170,0.1)",
        "linecolor": "rgba(136,153,170,0.2)",
    },
    "yaxis": {
        "gridcolor": "rgba(136,153,170,0.1)",
        "linecolor": "rgba(136,153,170,0.2)",
    },
    "margin": {"l": 50, "r": 30, "t": 40, "b": 40},
}


def _format_usd(value: int) -> str:
    if value >= 1_000_000:
        return f"${value / 1_000_000:.2f}M"
    if value >= 1_000:
        return f"${value / 1_000:.0f}k"
    return f"${value:,}"


def _kpi_card(
    label: str,
    value: str,
    color: str = "#00D4AA",
) -> str:
    return (
        f'<div style="background:rgba(26,42,58,0.55);'
        f'border:1px solid '
        f'rgba({_hex_rgb(color)},0.25);'
        f'border-radius:16px;'
        f'padding:20px 24px;text-align:center;">'
        f'<div style="font-size:0.75rem;font-weight:500;'
        f'color:#8899AA;letter-spacing:0.5px;'
        f'text-transform:uppercase;margin-bottom:6px;">'
        f'{label}</div>'
        f'<div style="font-size:1.8rem;font-weight:700;'
        f'color:{color};">{value}</div>'
        f'</div>'
    )


def _hex_rgb(hex_color: str) -> str:
    h = hex_color.lstrip("#")
    return (
        f"{int(h[0:2], 16)},"
        f"{int(h[2:4], 16)},"
        f"{int(h[4:6], 16)}"
    )


def render_analytics(
    hubs: pd.DataFrame,
    facilities: pd.DataFrame,
) -> None:
    """Affiche la page d'analyse du reseau."""

    st.header("Analyse du reseau")

    # --- Separation MASA / Zipline ---
    masa = hubs[hubs["Operateur"] == "MASA"].copy()
    zipline = hubs[hubs["Operateur"] == "Zipline"].copy()

    # --- Filtres (MASA uniquement) ---
    hub_types = sorted(masa["Type"].unique().tolist())
    selected_types = st.multiselect(
        "Types de hub MASA",
        options=hub_types,
        default=hub_types,
        key="filter_hub_type",
    )
    masa_f = masa[masa["Type"].isin(selected_types)].copy()

    # --- KPIs ---
    n_hubs_masa = len(masa_f)
    n_hubs_zl = len(zipline)
    n_drones = (
        int(masa_f["N_drones"].sum())
        if not masa_f.empty else 0
    )

    n_total_fac = len(facilities)
    n_covered_fac = int(facilities["Covered"].sum())
    couverture_pct = (
        round(100.0 * n_covered_fac / n_total_fac, 1)
        if n_total_fac else 0.0
    )

    n_fac_masa = int(
        facilities[
            facilities["Operateur"] == "MASA"
        ].shape[0]
    )
    n_fac_zl = int(
        facilities[
            facilities["Operateur"] == "Zipline"
        ].shape[0]
    )

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(
            _kpi_card(
                "Hubs MASA",
                str(n_hubs_masa),
                "#00D4AA",
            ),
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            _kpi_card("Drones", str(n_drones), "#4FC3F7"),
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            _kpi_card(
                "Couverture",
                f"{couverture_pct}%",
                "#FFA502",
            ),
            unsafe_allow_html=True,
        )
    with c4:
        st.markdown(
            _kpi_card(
                "Hubs Zipline",
                str(n_hubs_zl),
                "#FFB347",
            ),
            unsafe_allow_html=True,
        )

    st.markdown(
        "<div style='height:0.5rem;'></div>",
        unsafe_allow_html=True,
    )

    # Sous-KPIs facilities
    f1, f2, f3 = st.columns(3)
    f1.metric("Facilities MASA", n_fac_masa)
    f2.metric("Facilities Zipline", n_fac_zl)
    f3.metric(
        "Facilities hors couverture",
        n_total_fac - n_covered_fac,
    )

    st.markdown(
        "<div style='height:1rem;'></div>",
        unsafe_allow_html=True,
    )

    # --- Repartition MASA par type ---
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.subheader("Hubs MASA par type")
        if not masa_f.empty:
            type_counts = (
                masa_f["Type"]
                .value_counts()
                .reset_index()
            )
            type_counts.columns = ["Type", "Nombre"]

            color_map = {
                "Hauts_Flux": "#00D4AA",
                "Standard": "#4FC3F7",
                "Proximite": "#FFA502",
            }
            fig_types = px.pie(
                type_counts,
                names="Type",
                values="Nombre",
                color="Type",
                color_discrete_map=color_map,
                hole=0.45,
            )
            fig_types.update_traces(
                textposition="inside",
                textinfo="label+value",
                textfont_size=13,
            )
            fig_types.update_layout(
                showlegend=True,
                height=340,
                **_DARK_LAYOUT,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.15,
                    xanchor="center",
                    x=0.5,
                    font=dict(color="#E8EDF2"),
                ),
            )
            st.plotly_chart(
                fig_types, use_container_width=True,
            )
        else:
            st.info("Aucun hub MASA selectionne.")

    # --- Drones par type ---
    with col_chart2:
        st.subheader("Drones par type de hub")
        if not masa_f.empty:
            drones_by_type = (
                masa_f.groupby("Type")["N_drones"]
                .sum()
                .reset_index()
                .rename(columns={"N_drones": "Drones"})
            )
            color_map = {
                "Hauts_Flux": "#00D4AA",
                "Standard": "#4FC3F7",
                "Proximite": "#FFA502",
            }
            fig_drones = px.bar(
                drones_by_type,
                x="Type",
                y="Drones",
                color="Type",
                color_discrete_map=color_map,
                text_auto=True,
            )
            fig_drones.update_layout(
                showlegend=False,
                xaxis_title="",
                yaxis_title="Nombre de drones",
                height=340,
                **_DARK_LAYOUT,
            )
            st.plotly_chart(
                fig_drones, use_container_width=True,
            )
        else:
            st.info("Aucun hub MASA selectionne.")

    st.divider()

    # --- Repartition operateur (facilities) ---
    st.subheader("Facilities par operateur")
    op_counts = (
        facilities["Operateur"]
        .value_counts()
        .reset_index()
    )
    op_counts.columns = ["Operateur", "Nombre"]
    op_color_map = {
        "MASA": "#00D4AA",
        "Zipline": "#FFB347",
        "Aucun": "#E63946",
    }
    fig_op = px.bar(
        op_counts,
        x="Operateur",
        y="Nombre",
        color="Operateur",
        color_discrete_map=op_color_map,
        text_auto=True,
    )
    fig_op.update_layout(
        showlegend=False,
        xaxis_title="",
        yaxis_title="Nombre de facilities",
        height=340,
        **_DARK_LAYOUT,
    )
    st.plotly_chart(fig_op, use_container_width=True)

    st.divider()

    # --- Distribution des distances hub-facility ---
    st.subheader("Distance hub-facility (couvertes)")

    covered_fac = facilities[facilities["Covered"]].copy()
    if (
        "Dist_hub_km" in covered_fac.columns
        and not covered_fac.empty
    ):
        dist_mean = covered_fac["Dist_hub_km"].mean()
        dist_median = covered_fac["Dist_hub_km"].median()

        d1, d2, d3 = st.columns(3)
        d1.metric(
            "Distance moyenne", f"{dist_mean:.1f} km",
        )
        d2.metric(
            "Distance mediane", f"{dist_median:.1f} km",
        )
        d3.metric(
            "Facilities couvertes",
            f"{len(covered_fac):,}",
        )

        fig_dist = px.histogram(
            covered_fac,
            x="Dist_hub_km",
            color="Operateur",
            nbins=40,
            color_discrete_map=op_color_map,
            labels={
                "Dist_hub_km": "Distance au hub (km)",
            },
            barmode="overlay",
        )
        fig_dist.update_traces(opacity=0.75)
        fig_dist.add_vline(
            x=30.0,
            line_dash="dash",
            line_color="#00D4AA",
            annotation_text="MASA 30 km",
            annotation_position="top left",
            annotation_font_color="#00D4AA",
        )
        fig_dist.add_vline(
            x=80.0,
            line_dash="dash",
            line_color="#FFB347",
            annotation_text="Zipline 80 km",
            annotation_position="top right",
            annotation_font_color="#FFB347",
        )
        fig_dist.update_layout(
            yaxis_title="Nombre de facilities",
            height=380,
            **_DARK_LAYOUT,
            legend=dict(
                font=dict(color="#E8EDF2"),
            ),
        )
        st.plotly_chart(
            fig_dist, use_container_width=True,
        )
    else:
        st.info("Pas de donnees de distance.")

    st.divider()

    # --- Budget (MASA uniquement) ---
    st.subheader("Budget MASA")
    st.caption(
        "Budget pour les 25 hubs MASA uniquement. "
        "Zipline est un operateur tiers."
    )

    if not masa_f.empty:
        budget_df = masa_f[
            ["Hub_ID", "Type", "CAPEX_USD", "OPEX_annuel_USD"]
        ].copy()
        budget_df["Hub_ID"] = budget_df["Hub_ID"].astype(int)
        budget_df = budget_df.sort_values(by="Hub_ID")

        labels = [
            f"Hub {h}" for h in budget_df["Hub_ID"]
        ]

        fig_budget = go.Figure()
        fig_budget.add_trace(go.Bar(
            name="CAPEX",
            x=labels,
            y=budget_df["CAPEX_USD"],
            marker_color="#00D4AA",
            text=[
                _format_usd(v)
                for v in budget_df["CAPEX_USD"]
            ],
            textposition="outside",
            textfont=dict(size=11),
        ))
        fig_budget.add_trace(go.Bar(
            name="OPEX annuel",
            x=labels,
            y=budget_df["OPEX_annuel_USD"],
            marker_color="#4FC3F7",
            text=[
                _format_usd(v)
                for v in budget_df["OPEX_annuel_USD"]
            ],
            textposition="outside",
            textfont=dict(size=11),
        ))
        fig_budget.update_layout(
            barmode="group",
            yaxis_title="USD",
            height=420,
            **_DARK_LAYOUT,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                font=dict(color="#E8EDF2"),
            ),
        )
        st.plotly_chart(
            fig_budget, use_container_width=True,
        )

        capex_total = int(masa_f["CAPEX_USD"].sum())
        opex_total = int(
            masa_f["OPEX_annuel_USD"].sum()
        )
        tco_5ans = capex_total + opex_total * 5

        b1, b2, b3 = st.columns(3)
        with b1:
            st.markdown(
                _kpi_card(
                    "CAPEX total",
                    _format_usd(capex_total),
                    "#00D4AA",
                ),
                unsafe_allow_html=True,
            )
        with b2:
            st.markdown(
                _kpi_card(
                    "OPEX annuel",
                    _format_usd(opex_total),
                    "#4FC3F7",
                ),
                unsafe_allow_html=True,
            )
        with b3:
            st.markdown(
                _kpi_card(
                    "TCO 5 ans",
                    _format_usd(tco_5ans),
                    "#FFA502",
                ),
                unsafe_allow_html=True,
            )

    st.divider()

    # --- Tableau recapitulatif ---
    st.subheader("Detail des hubs")

    all_hubs = pd.concat(
        [masa_f, zipline], ignore_index=True,
    )
    display_cols = [
        "Hub_ID", "Operateur", "Type",
        "Latitude", "Longitude",
        "N_drones", "N_facilities",
        "CAPEX_USD", "OPEX_annuel_USD",
    ]
    cols_present = [
        c for c in display_cols if c in all_hubs.columns
    ]
    table_df = all_hubs[cols_present].copy()
    table_df["Hub_ID"] = table_df["Hub_ID"].astype(int)
    table_df = table_df.sort_values(
        by="Hub_ID",
    ).reset_index(drop=True)

    rename_map = {
        "Hub_ID": "Hub",
        "N_drones": "Drones",
        "N_facilities": "Facilities",
        "CAPEX_USD": "CAPEX ($)",
        "OPEX_annuel_USD": "OPEX/an ($)",
    }
    table_df = table_df.rename(columns=rename_map)

    fmt_cols: dict[str, str] = {}
    if "Latitude" in table_df.columns:
        fmt_cols["Latitude"] = "%.4f"
    if "Longitude" in table_df.columns:
        fmt_cols["Longitude"] = "%.4f"

    column_config: dict = {}
    if "CAPEX ($)" in table_df.columns:
        column_config["CAPEX ($)"] = (
            st.column_config.NumberColumn(format="$%d")
        )
    if "OPEX/an ($)" in table_df.columns:
        column_config["OPEX/an ($)"] = (
            st.column_config.NumberColumn(format="$%d")
        )

    st.dataframe(
        table_df.style.format(fmt_cols, na_rep="---"),
        use_container_width=True,
        hide_index=True,
        column_config=column_config,
        height=min(500, 40 + 35 * len(table_df)),
    )
