# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags

def clean_price(price):
    price = price.replace("$","")
    price = price.replace("\xa0-\xa0", "|")
    if "|" not in price: return price.strip()
    return price.split("|")[0].strip()

def full_url_out(urls):
    if "https" in urls[0]: return urls[0]
    url = f"{urls[1]}{urls[0]}"
    return url

def clean_JSON_LD(jld):
    if "description" in jld:
        jld["description"] = jld["description"].replace("\r","").replace("\n","").replace("\t","")
    return jld

class CC_Meta_Cluster_JSON_LD(scrapy.Item):
    # define the fields for your item here like:
    cluster_id     = scrapy.Field( output_processor = TakeFirst())
    json_ld        = scrapy.Field( output_processor = TakeFirst())
    json_ld        = scrapy.Field(input_processor = MapCompose(clean_JSON_LD), output_processor = TakeFirst())


class CC_IDX_RECORD(scrapy.Item):
    # define the fields for your item here like:
    cc_idx_record  = scrapy.Field( output_processor = TakeFirst())
