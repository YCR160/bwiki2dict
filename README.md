# bwiki2dict

使用 BWIKI 生成游戏词典

```sh
pip install mw2fcitx
```

## 使用

```sh
mw2fcitx -c config_script.py
```

## api

https://wiki.biligame.com/sr/api.php?action=query&generator=allpages&prop=categories&format=json&gaplimit=500&cllimit=500&gapcontinue=一封未寄出的信&clcontinue=10318|事件

- `https://wiki.biligame.com/arknights/api.php` 百科网站的 MediaWiki API 路径
- `action=query` [查询操作](https://www.mediawiki.org/wiki/API:Query)，[可选操作](https://www.mediawiki.org/wiki/API:Main_page)大部分都是管理操作
- `generator=allpages` [生成器](https://www.mediawiki.org/wiki/API:Query#Generators)用于生成一系列页面的属性，比如页面+分类
- `prop=categories` 附加属性，获取页面的分类，后续通过筛选类别缩减词库规模
- `format=json` 返回格式为 JSON
- `gaplimit=500` 生成器（gap:generator=allpages）的最大数量，1-500，默认 10
- `cllimit=500` [分类](https://www.mediawiki.org/w/api.php?action=help&modules=query%2Bcategories)（cl:prop=categories）的最大数量，1-500，默认 10
- `gapcontinue=一封未寄出的信` 生成器[继续](https://www.mediawiki.org/wiki/API:Continue)的起始页面
- `clcontinue=10318|事件` 分类继续的起始分类

当返回的页面达到 cllimit，但因为分类超过了 clcontinue，返回结果的部分页面不带有分类，此时 continue 字段包含 clcontinue，用于在下一次请求从被截断的分类继续。

```json
// https://wiki.biligame.com/sr/api.php?action=query&generator=allpages&prop=categories&format=json
{
    "continue": {
        "clcontinue": "4291|正在计时的页面",
        "continue": "||"
    },
    "query": {
        "pages": {
            "406": {
                "pageid": 406,
                "ns": 0,
                "title": "1.0版本「通往群星的轨道」前瞻直播总结",
                "categories": [
                    {
                        "ns": 14,
                        "title": "分类:正在计时的页面"
                    },
                    {
                        "ns": 14,
                        "title": "分类:版本更新"
                    }
                ]
            },
            // ...
            "4291": {
                "pageid": 4291,
                "ns": 0,
                "title": "1.2版本「仙骸有终」更新专题",
                "categories": [
                    {
                        "ns": 14,
                        "title": "分类:含有受损文件链接的页面"
                    }
                    // <--- 在这里被截断，"clcontinue": "4291|正在计时的页面"
                ]
            },
            // ...
        }
    }
}
```

而当返回的页面达到 cllimit，分类也在 clcontinue 之内，返回内容包含 batchcomplete 字段，continue 字段包含 gapcontinue，用于在下一次请求从之后的页面继续。

```json
// https://wiki.biligame.com/sr/api.php?action=query&generator=allpages&prop=categories&format=json&clcontinue=7059|正在计时的页面
{
    "batchcomplete": "",
    "continue": {
        "gapcontinue": "1.5版本「迷离幻夜谈」更新专题",
        "continue": "gapcontinue||"
    },
    "query": {
        "pages": {
            "406": {
                "pageid": 406,
                "ns": 0,
                "title": "1.0版本「通往群星的轨道」前瞻直播总结"
                // <--- clcontinue=7059|正在计时的页面 之前的不显示分类
            },
            // ...
            "10321": {
                "pageid": 10321,
                "ns": 0,
                "title": "*完美*大挑战！",
                "categories": [
                    {
                        "ns": 14,
                        "title": "分类:事件"
                    }
                ]
            }
        }
    }
}
```
