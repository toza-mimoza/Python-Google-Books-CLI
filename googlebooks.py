import json 

import click
import requests
import webbrowser

__author__ = "toza-mimoza"

@click.group()
def main():
    """
    CLI for querying books on Google Books by toza-mimoza
    """
    pass

@main.command()
@click.argument('query')
def search(query):
    """This search and return results corresponding to the given query from Google Books"""
    url_format = 'https://www.googleapis.com/books/v1/volumes'
    query = "+".join(query.split())

    query_params = {
        'q': query
    }
    
    response = requests.get(url_format, params=query_params)
    #resp_list=[requests.get(url_format,params=query_params)]
    
    responseInJSON=response.json()
    with open('searchQuery.json','w') as json_file: #stores a query
        json.dump(responseInJSON,json_file)

    
   # click.echo(json.dumps(responseInJSON,indent=10))
    for i in range(len(responseInJSON['items'])):
        volInfo=responseInJSON['items'][i]['volumeInfo']
        salInfo=responseInJSON['items'][i]['saleInfo']
        accInfo=responseInJSON['items'][i]['accessInfo']

        click.echo("__________________________________________________________________________________")
        click.echo("Title:\t\t "+volInfo['title'])
        
        if ('subtitle' in volInfo):
            click.echo("    "+str(volInfo['subtitle']))
        if('description' in volInfo):
            click.echo("Description:\t "+volInfo['description'])
        if ('authors' not in volInfo):
            click.echo("Authors:\t UNKNOWN")
            pass
        elif len(volInfo['authors'])==1:
            click.echo("Author:\t\t "+str(volInfo['authors'][0]))
        elif len(volInfo['authors'])>1:
            for author in volInfo['authors']:
                click.echo("Author:\t\t "+author)
                pass
            pass
        if ('publishedDate' not in volInfo):
             click.echo("Published date:\t UNKNOWN")
        else:
            click.echo("Published date:\t "+volInfo['publishedDate'])
        if ('pageCount' not in volInfo):
            click.echo("Page count:\t UNKNOWN") 
        else: 
            click.echo("Page count:\t "+str(volInfo['pageCount']))
        click.echo("Language:\t "+volInfo['language'])
        click.echo("Sale Info: ")
        click.echo("    Country:\t "+salInfo['country'])
        if salInfo['saleability']=='FOR_SALE':
            click.echo("    Price:\t "+str(salInfo['retailPrice']['amount'])+" "+salInfo['retailPrice']['currencyCode'])
            if salInfo['retailPrice']['amount']==0.0:
                click.echo("    Opening...")
                url=accInfo['webReaderLink']
                chrome_path="C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
                webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))
                webbrowser.get('chrome').open_new_tab(url)
                
        elif salInfo['saleability']=='FREE':
            click.echo("    Price:\t The book is FREE!")
           
            
            click.echo("    Opening...")
            if 'downloadLink' not in accInfo['pdf']:
                click.echo("NO DOWNLOAD LINK...")
                if 'webReaderLink' not in accInfo:
                    click.echo("NO WEB READER LINK")
                    pass
                
                else:
                    url=accInfo['webReaderLink']
                    chrome_path="C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
                    webbrowser.register('chrome', None,webbrowser.BackgroundBrowser(chrome_path))
                    webbrowser.get('chrome').open_new_tab(url)
           
                    pass
            else:
                url=accInfo['pdf']['downloadLink']
                # file_name=volInfo['title'] #later for naming the downloaded file 
            
                chrome_path="C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
                webbrowser.register('chrome', None,webbrowser.BackgroundBrowser(chrome_path))
                webbrowser.get('chrome').open_new_tab(url)
            pass
        elif salInfo['saleability']=='NOT_FOR_SALE':
            click.echo("    Price:\t NOT FOR SALE")
            pass
        pass

  

    
@main.command()
@click.argument('id')
def get(id):
    """This return a particular book from the given id on Google Books"""
    url_format = 'https://www.googleapis.com/books/v1/volumes/{}'
    click.echo(id)

    response = requests.get(url_format.format(id))
    responseInJSON=response.json()
    with open('searchQuery.json','w') as json_file: #stores a query
        json.dump(responseInJSON,json_file)

    for i in range(len(responseInJSON['items'])):
        volInfo=responseInJSON['items'][i]['volumeInfo']
        salInfo=responseInJSON['items'][i]['saleInfo']
        accInfo=responseInJSON['items'][i]['accessInfo']

        click.echo("__________________________________________________________________________________")
        click.echo("Title:\t\t "+volInfo['title'])
        
        if ('subtitle' in volInfo):
            click.echo("    "+str(volInfo['subtitle']))
        if ('authors' not in volInfo):
            click.echo("Authors:\t UNKNOWN")
            pass
        elif len(volInfo['authors'])==1:
            click.echo("Author:\t\t "+str(volInfo['authors'][0]))
        elif len(volInfo['authors'])>1:
            for author in volInfo['authors']:
                click.echo("Author:\t\t "+author)
                pass
            pass
        if ('publishedDate' not in volInfo):
             click.echo("Published date:\t UNKNOWN")
        else:
            click.echo("Published date:\t "+volInfo['publishedDate'])
        if ('pageCount' not in volInfo):
            click.echo("Page count:\t UNKNOWN") 
        else: 
            click.echo("Page count:\t "+str(volInfo['pageCount']))
        click.echo("Language:\t "+volInfo['language'])
        click.echo("Sale Info: ")
        click.echo("    Country:\t "+salInfo['country'])
        if salInfo['saleability']=='FOR_SALE':
            click.echo("    Price:\t "+str(salInfo['retailPrice']['amount'])+" "+salInfo['retailPrice']['currencyCode'])
            pass
        elif salInfo['saleability']=='FREE':
            click.echo("    Price:\t The book is FREE!")
            ######
            click.echo("    Downloading...")
            url=accInfo['pdf']['downloadLink']
            file_name=volInfo['title']
            
            r=requests.get(url)
            with open(file_name+".pdf", "wb") as code:
               code.write(r.content)
               pass 
            click.echo("File downloaded! ")
            ######
            pass
        elif salInfo['saleability']=='NOT_FOR_SALE':
            click.echo("    Price:\t NOT FOR SALE")
            pass
        pass
  


if __name__ == "__main__":
    main()