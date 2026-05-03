def render_cards(cards):
    html = ""
    for c in cards:
        color = "red" if c in ['10','J','Q','K','A'] else "black"

        html += f"""
        <div style="
            display:inline-block;
            width:40px;
            height:55px;
            margin:3px;
            border:2px solid black;
            border-radius:4px;
            background:white;
            font-family:monospace;
            font-size:16px;
            font-weight:bold;
            color:{color};
            text-align:center;
            line-height:55px;
            box-shadow:2px 2px 0px #000;
        ">
            {c}
        </div>
        """
    return html