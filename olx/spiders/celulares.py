# -*- coding: utf-8 -*-
import scrapy


class CelularesSpider(scrapy.Spider):
    name = 'celulares'
    allowed_domains = ['pe.olx.com.br']
    start_urls = ['http://pe.olx.com.br/celulares/']

    def parse(self, response):
        items = response.xpath(
            '//ul[@id="main-ad-list"]/li[not(contains(@class, "list_native"))]'
            #nao pega anuncio
            )
        
        for item in items:
            url = item.xpath('./a/@href').extract_first()
            yield scrapy.Request(url = url, callback = self.parse_detail)
        next_page = response.xpath('//div[contains(@class, "module_pagination")]//a[@rel = "next"]/@href')
        #vou para proxima pagina
        if next_page:
            #self.log('PROXIMA PAGE: {}'.format(next_page.extract_first()))
            yield scrapy.Request(
                url=next_page.extract_first(), callback = self.parse
                #pego os itens
            )

    def parse_detail(self, response):
        title = response.xpath('//title/text()').extract_first()
        tipo = response.xpath('//span[contains(text(), "Tipo")]/following-sibling::strong/text()').extract_first()    
        estado = response.xpath('//span[contains(text(), "Novo/Usado")]/following-sibling::strong/text()').extract_first()
        municipio = response.xpath('//span[contains(text(), "Município")]/following-sibling::strong/text()').extract_first()
        cep = response.xpath('//span[contains(text(), "CEP")]/following-sibling::strong/text()').extract_first()
        bairro = response.xpath('//span[contains(text(), "Bairro")]/following-sibling::strong/text()').extract_first()
        yield{
            'title': title,
            'tipo': tipo,
            'estado': estado,
            'municipio': municipio,
            'cep': cep,
            'bairro': bairro,
            }
