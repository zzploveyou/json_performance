# serialize and deserialize for many times
| Module     | serialize | deserialize | total |
| ---------- | --------- | ----------- | ----- |
| yajl       | 0.122     | 0.137       | 0.260 |
| ujson      | 0.090     | 0.078       | 0.168 |
| simplejson | 0.648     | 0.451       | 1.099 |
| json       | 0.402     | 0.322       | 0.724 |


# Read and Write big json file

comparation between json and ujson[test size: 30]:

| Module | Read  | Write  |
| ------ | ----- | ------ |
| json   | 5.616 | 22.115 |
| ujson  | 6.820 | 9.241  |

So choose [ujson](https://github.com/esnme/ultrajson/) version >= 2.0
