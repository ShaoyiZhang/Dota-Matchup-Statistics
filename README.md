# Dota-Matchup-Statistics
To run the crawler:

    python3 crawler.py

There is a sleep(0.5) operation during each web query, so the crawling part will take few minutes.

Example:

    json['abaddon'] = 
        "abaddon": {
            "Ally": {
                "abaddon": {
                    "abyssal_underlord": {
                        "co-opIndex": "-5.38",
                        "winRateAsAlly": "55.24"
                    },
                    ......
                    "zuus": {
                        "co-opIndex": "0.00",
                        "winRateAsAlly": "62.22"
                    }
                }
            },
            "Enemy": {
                "abaddon": {
                    "abyssal_underlord": {
                        "co-opIndex": "-2.75",
                        "winRateAsAlly": "52.47"
                    },
                    ......
                    "zuus": {
                        "co-opIndex": "-0.58",
                        "winRateAsAlly": "49.66"
                    }
                }
            },
            "winRate": "56.18"
        }


