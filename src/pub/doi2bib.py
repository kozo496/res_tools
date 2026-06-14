#!/usr/bin/env python3
# TODO: Fix get_bibtex_from_pmid to use efetch instead of esearch, and to handle multiple PMIDs

import sys
import argparse
from urllib import request, error
import xml.etree.ElementTree as ET

def get_bibtex(doi,ispreprint):
    # Copied from: https://arumoy.me/blogs/doi2bib/
    if ispreprint:
        url = f"https://arxiv.org/bibtex/{doi}"
    else:
        url = f"https://api.crossref.org/works/{doi}/transform/application/x-bibtex"
    req = request.Request(url)

    try:
        with request.urlopen(req) as response:
            return response.read().decode()
    except error.HTTPError as e:
        return f"HTTP Error: {e.code}"
    except error.URLError as e:
        return f"URL Error: {e.reason}"
    

def get_bibtex_from_pmid(pmid):
    # NCBI E-utilities efetch endpoint for PubMed
    # url = f"https://nih.gov{pmid}&retmode=xml"
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={pmid}&retmode=xml"
    
    try:
        # Request data using Python's built-in urllib
        with request.urlopen(url) as response:
            xml_data = response.read()
            
        # Parse XML root
        root = ET.fromstring(xml_data)
        article = root.find(".//PubmedArticle")
        
        if article is None:
            return f"% Error: No article found for PMID {pmid}"
            
        # Extract basic bibliographic metadata
        title = article.find(".//ArticleTitle").text if article.find(".//ArticleTitle") is not None else ""
        journal = article.find(".//Journal/Title").text if article.find(".//Journal/Title") is not None else ""
        year = article.find(".//JournalIssue/PubDate/Year").text if article.find(".//JournalIssue/PubDate/Year") is not None else "0000"
        volume = article.find(".//JournalIssue/Volume").text if article.find(".//JournalIssue/Volume") is not None else ""
        issue = article.find(".//JournalIssue/Issue").text if article.find(".//JournalIssue/Issue") is not None else ""
        pages = article.find(".//MedlinePgn").text if article.find(".//MedlinePgn") is not None else ""
        
        # Format Author list (Lastname Initials)
        authors_list = []
        for author in article.findall(".//AuthorList/Author"):
            last_name = author.find("LastName")
            initials = author.find("Initials")
            if last_name is not None and initials is not None:
                authors_list.append(f"{last_name.text}, {initials.text}")
        authors = " and ".join(authors_list)
        
        # Grab first author's last name for the citation key
        first_author = article.find(".//AuthorList/Author[1]/LastName")
        cite_key = f"{first_author.text.lower()}{year}" if first_author is not None else f"pmid{pmid}"
        
        # Construct BibTeX string
        bibtex = f"@article{{{cite_key},\n"
        bibtex += f"  author  = {{{authors}}},\n"
        bibtex += f"  title   = {{{title}}},\n"
        bibtex += f"  journal = {{{journal}}},\n"
        bibtex += f"  year    = {{{year}}},\n"
        if volume: bibtex += f"  volume  = {{{volume}}},\n"
        if issue:  bibtex += f"  number  = {{{issue}}},\n"
        if pages:  bibtex += f"  pages   = {{{pages}}},\n"
        bibtex += f"  note    = {{PMID: {pmid}}}\n"
        bibtex += "}"
        
        return bibtex

    except Exception as e:
        return f"% Error fetching data: {str(e)}"

# # Example Usage
# pmid_input = "30440093"
# print(get_bibtex_from_pmid(pmid_input))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            description="Convert DOI or Arxiv ID to Bibtex"
            )
    parser.add_argument(
            "doi",
            help="DOI or Arxiv ID of paper"
            )
    parser.add_argument(
            "-p",
            "--preprint",
            help="Treat provided DOI as Arxiv ID",
            action="store_true",
            default=False,
            )
    args = parser.parse_args()

    bibtex = get_bibtex(args.doi, args.preprint)
    print(bibtex)
