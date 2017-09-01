TESTS = {
  "rndrw": "Random reads/writes"
};
METRICS = {
  "total_num_events": "Total number of events",
  "req_95p": "95th percentile latency",
  "req_avg": "Avg. latency",
  "req_max": "Max. latency",
  "req_min": "Min. latency",
  "nother": "Queries other",
  "nread": "Queries read",
  "ntotal": "Queries total",
  "nwrite": "Queries write",
  "nqueries": "Queries/s",
  "ierrors": "Ignored errors/s",
  "transactions": "Transactions/s",
  "tevents": "Thread events"
}
results = {
  "mariadb": {
    "rndrw": {
      "results": {
        "total_num_events": {
          "1024": [
            4363
          ],
          "768": [
            3534
          ],
          "512": [
            3924
          ],
          "256": [
            4073
          ],
          "128": [
            3619
          ],
          "64": [
            3377
          ],
          "32": [
            3003
          ],
          "16": [
            2301
          ],
          "8": [
            1513
          ],
          "4": [
            895
          ],
          "2": [
            480
          ],
          "1": [
            242
          ]
        },
        "req_95p": {
          "1024": [
            14827.42
          ],
          "768": [
            15650.42
          ],
          "512": [
            7754.26
          ],
          "256": [
            3326.55
          ],
          "128": [
            1803.47
          ],
          "64": [
            909.8
          ],
          "32": [
            411.96
          ],
          "16": [
            277.21
          ],
          "8": [
            223.34
          ],
          "4": [
            200.47
          ],
          "2": [
            189.93
          ],
          "1": [
            189.93
          ]
        },
        "req_avg": {
          "1024": [
            7775.12
          ],
          "768": [
            6750.53
          ],
          "512": [
            4089.92
          ],
          "256": [
            1924.71
          ],
          "128": [
            1073.56
          ],
          "64": [
            572.09
          ],
          "32": [
            320.67
          ],
          "16": [
            209.4
          ],
          "8": [
            159.16
          ],
          "4": [
            134.32
          ],
          "2": [
            125.19
          ],
          "1": [
            124.31
          ]
        },
        "req_max": {
          "1024": [
            39392.03
          ],
          "768": [
            20565.54
          ],
          "512": [
            17336.77
          ],
          "256": [
            10488.02
          ],
          "128": [
            3570.09
          ],
          "64": [
            1353.63
          ],
          "32": [
            1072.75
          ],
          "16": [
            344.08
          ],
          "8": [
            304.79
          ],
          "4": [
            274.62
          ],
          "2": [
            257.68
          ],
          "1": [
            262.35
          ]
        },
        "req_min": {
          "1024": [
            1148.05
          ],
          "768": [
            625.9
          ],
          "512": [
            360.08
          ],
          "256": [
            590.71
          ],
          "128": [
            428.94
          ],
          "64": [
            261.05
          ],
          "32": [
            190.77
          ],
          "16": [
            125.59
          ],
          "8": [
            101.09
          ],
          "4": [
            87.71
          ],
          "2": [
            78.98
          ],
          "1": [
            76.49
          ]
        },
        "nother": {
          "1024": [
            8729
          ],
          "768": [
            7069
          ],
          "512": [
            7848
          ],
          "256": [
            8147
          ],
          "128": [
            7238
          ],
          "64": [
            6755
          ],
          "32": [
            6006
          ],
          "16": [
            4602
          ],
          "8": [
            3026
          ],
          "4": [
            1790
          ],
          "2": [
            960
          ],
          "1": [
            484
          ]
        },
        "nread": {
          "1024": [
            61124
          ],
          "768": [
            49490
          ],
          "512": [
            54936
          ],
          "256": [
            57036
          ],
          "128": [
            50666
          ],
          "64": [
            47292
          ],
          "32": [
            42042
          ],
          "16": [
            32214
          ],
          "8": [
            21182
          ],
          "4": [
            12530
          ],
          "2": [
            6720
          ],
          "1": [
            3388
          ]
        },
        "ntotal": {
          "1024": [
            87310
          ],
          "768": [
            70696
          ],
          "512": [
            78480
          ],
          "256": [
            81477
          ],
          "128": [
            72380
          ],
          "64": [
            67557
          ],
          "32": [
            60060
          ],
          "16": [
            46020
          ],
          "8": [
            30260
          ],
          "4": [
            17900
          ],
          "2": [
            9600
          ],
          "1": [
            4840
          ]
        },
        "nwrite": {
          "1024": [
            17457
          ],
          "768": [
            14137
          ],
          "512": [
            15696
          ],
          "256": [
            16294
          ],
          "128": [
            14476
          ],
          "64": [
            13510
          ],
          "32": [
            12012
          ],
          "16": [
            9204
          ],
          "8": [
            6052
          ],
          "4": [
            3580
          ],
          "2": [
            1920
          ],
          "1": [
            968
          ]
        },
        "nqueries": {
          "1024": [
            1823.66
          ],
          "768": [
            2063.98
          ],
          "512": [
            2171.29
          ],
          "256": [
            2583.88
          ],
          "128": [
            2346.99
          ],
          "64": [
            2204.63
          ],
          "32": [
            1982.14
          ],
          "16": [
            1524.23
          ],
          "8": [
            1003.44
          ],
          "4": [
            595.01
          ],
          "2": [
            319.46
          ],
          "1": [
            160.86
          ]
        },
        "ierrors": {
          "1024": [
            0.06
          ],
          "768": [
            0.03
          ],
          "512": [
            0.00
          ],
          "256": [
            0.03
          ],
          "128": [
            0.00
          ],
          "64": [
            0.03
          ],
          "32": [
            0.00
          ],
          "16": [
            0.00
          ],
          "8": [
            0.00
          ],
          "4": [
            0.00
          ],
          "2": [
            0.00
          ],
          "1": [
            0.00
          ]
        },
        "transactions": {
          "1024": [
            91.13
          ],
          "768": [
            103.18
          ],
          "512": [
            108.56
          ],
          "256": [
            129.17
          ],
          "128": [
            117.35
          ],
          "64": [
            110.20
          ],
          "32": [
            99.11
          ],
          "16": [
            76.21
          ],
          "8": [
            50.17
          ],
          "4": [
            29.75
          ],
          "2": [
            15.97
          ],
          "1": [
            8.04
          ]
        },
        "tevents": {}
      },
      "averages": {
        "total_num_events": [
          [
            1,
            242
          ],
          [
            2,
            480
          ],
          [
            4,
            895
          ],
          [
            8,
            1513
          ],
          [
            16,
            2301
          ],
          [
            32,
            3003
          ],
          [
            64,
            3377
          ],
          [
            128,
            3619
          ],
          [
            256,
            4073
          ],
          [
            512,
            3924
          ],
          [
            768,
            3534
          ],
          [
            1024,
            4363
          ]
        ],
        "req_95p": [
          [
            1,
            189
          ],
          [
            2,
            189
          ],
          [
            4,
            200
          ],
          [
            8,
            223
          ],
          [
            16,
            277
          ],
          [
            32,
            411
          ],
          [
            64,
            909
          ],
          [
            128,
            1803
          ],
          [
            256,
            3326
          ],
          [
            512,
            7754
          ],
          [
            768,
            15650
          ],
          [
            1024,
            14827
          ]
        ],
        "req_avg": [
          [
            1,
            124
          ],
          [
            2,
            125
          ],
          [
            4,
            134
          ],
          [
            8,
            159
          ],
          [
            16,
            209
          ],
          [
            32,
            320
          ],
          [
            64,
            572
          ],
          [
            128,
            1073
          ],
          [
            256,
            1924
          ],
          [
            512,
            4089
          ],
          [
            768,
            6750
          ],
          [
            1024,
            7775
          ]
        ],
        "req_max": [
          [
            1,
            262
          ],
          [
            2,
            257
          ],
          [
            4,
            274
          ],
          [
            8,
            304
          ],
          [
            16,
            344
          ],
          [
            32,
            1072
          ],
          [
            64,
            1353
          ],
          [
            128,
            3570
          ],
          [
            256,
            10488
          ],
          [
            512,
            17336
          ],
          [
            768,
            20565
          ],
          [
            1024,
            39392
          ]
        ],
        "req_min": [
          [
            1,
            76
          ],
          [
            2,
            78
          ],
          [
            4,
            87
          ],
          [
            8,
            101
          ],
          [
            16,
            125
          ],
          [
            32,
            190
          ],
          [
            64,
            261
          ],
          [
            128,
            428
          ],
          [
            256,
            590
          ],
          [
            512,
            360
          ],
          [
            768,
            625
          ],
          [
            1024,
            1148
          ]
        ],
        "nother": [
          [
            1,
            484
          ],
          [
            2,
            960
          ],
          [
            4,
            1790
          ],
          [
            8,
            3026
          ],
          [
            16,
            4602
          ],
          [
            32,
            6006
          ],
          [
            64,
            6755
          ],
          [
            128,
            7238
          ],
          [
            256,
            8147
          ],
          [
            512,
            7848
          ],
          [
            768,
            7069
          ],
          [
            1024,
            8729
          ]
        ],
        "nread": [
          [
            1,
            3388
          ],
          [
            2,
            6720
          ],
          [
            4,
            12530
          ],
          [
            8,
            21182
          ],
          [
            16,
            32214
          ],
          [
            32,
            42042
          ],
          [
            64,
            47292
          ],
          [
            128,
            50666
          ],
          [
            256,
            57036
          ],
          [
            512,
            54936
          ],
          [
            768,
            49490
          ],
          [
            1024,
            61124
          ]
        ],
        "ntotal": [
          [
            1,
            4840
          ],
          [
            2,
            9600
          ],
          [
            4,
            17900
          ],
          [
            8,
            30260
          ],
          [
            16,
            46020
          ],
          [
            32,
            60060
          ],
          [
            64,
            67557
          ],
          [
            128,
            72380
          ],
          [
            256,
            81477
          ],
          [
            512,
            78480
          ],
          [
            768,
            70696
          ],
          [
            1024,
            87310
          ]
        ],
        "nwrite": [
          [
            1,
            968
          ],
          [
            2,
            1920
          ],
          [
            4,
            3580
          ],
          [
            8,
            6052
          ],
          [
            16,
            9204
          ],
          [
            32,
            12012
          ],
          [
            64,
            13510
          ],
          [
            128,
            14476
          ],
          [
            256,
            16294
          ],
          [
            512,
            15696
          ],
          [
            768,
            14137
          ],
          [
            1024,
            17457
          ]
        ],
        "nqueries": [
          [
            1,
            160
          ],
          [
            2,
            319
          ],
          [
            4,
            595
          ],
          [
            8,
            1003
          ],
          [
            16,
            1524
          ],
          [
            32,
            1982
          ],
          [
            64,
            2204
          ],
          [
            128,
            2346
          ],
          [
            256,
            2583
          ],
          [
            512,
            2171
          ],
          [
            768,
            2063
          ],
          [
            1024,
            1823
          ]
        ],
        "ierrors": [
          [
            1,
            0
          ],
          [
            2,
            0
          ],
          [
            4,
            0
          ],
          [
            8,
            0
          ],
          [
            16,
            0
          ],
          [
            32,
            0
          ],
          [
            64,
            0
          ],
          [
            128,
            0
          ],
          [
            256,
            0
          ],
          [
            512,
            0
          ],
          [
            768,
            0
          ],
          [
            1024,
            0
          ]
        ],
        "transactions": [
          [
            1,
            8
          ],
          [
            2,
            15
          ],
          [
            4,
            29
          ],
          [
            8,
            50
          ],
          [
            16,
            76
          ],
          [
            32,
            99
          ],
          [
            64,
            110
          ],
          [
            128,
            117
          ],
          [
            256,
            129
          ],
          [
            512,
            108
          ],
          [
            768,
            103
          ],
          [
            1024,
            91
          ]
        ],
        "tevents": []
      }
    }
  }
};