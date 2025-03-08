from pybtex.database.input import bibtex

def get_personal_data():
    name = ['Da "Alex"', "Yan"]
    email = "alexyan1987@outlook.com"
    scholar = "28WTkNkAAAAJ"
    twitter = "aiezue"
    orcid = "0000-0002-1265-9772"
    github = "fabea"

    bio_text = f"""
                <p>
                I (<ruby>闫<rt>Yán</rt></ruby> <ruby>达<rt>Dá</rt></ruby>; Alex Yan),PhD, work on assessment and feedback, and educational application of (Gen)AI. </p>
                <p>I have been teaching in <a href="https://www.xyafu.edu.cn" target="_blank"> Xinyang Agriculture and Forestry University</a> since 2013. My research interests are language learning; formative assessment; translation/interpreting studies; and human-computer interaction.
                </p>
                """
    social_media = f"""
                <p>
                <button class="btn btn-link h-100" type="button" data-toggle="collapse" data-target="#demo" style="margin-left: 0px; margin-top: -1px; margin-right: 5px;" aria-expanded="true"><i class="fa-solid fa-graduation-cap"></i>About Me</button>
                <a href="https://870603.xyz/assets/pdf/CV.pdf" target="_blank" style="margin-right: 5px"><i class="fa fa-address-card fa-lg"></i> CV</a>
                <a href="mailto:{email}" style="margin-right: 5px"><i class="far fa-envelope-open fa-lg"></i> Mail</a>
                <a href="https://scholar.google.com/citations?user={scholar}&hl=en" target="_blank" style="margin-right: 5px"><i class="fa-brands fa-google-scholar"></i> Scholar</a>
                <a href="https://orcid.org/{orcid}" target="_blank" style="margin-right: 5px"><i class="fa-brands fa-orcid"></i> ORCiD</a>
                </p>
    """
    bio = """
                    <div id="demo" class="collapse">
                    <span style="font-weight: bold;">Bio:</span>
                    I am currently pursuing a PhD in Translation (2022–2024) at the <a href="https://www.usm.my/" target="_blank">University of Science, Malaysia (USM)</a>. I hold a Master’s degree in Translation (2010–2013) from <a href="https://www.wzu.edu.cn/" target="_blank">Wenzhou University</a> 
                    and a Bachelor’s degree in English (2004–2008) from 
                    <a href="https://www.haust.edu.cn/" target="_blank">Henan University of Science and Technology</a>. 
                    With over a decade of teaching experience at 
                    <a href="https://www.xyafu.edu.cn/" target="_blank">Xinyang Agriculture and Forestry University (XYAFU)</a>, 
                    I played a key role in establishing the university's Bachelor of Translation and Interpreting (BTI) program. 
                    I have taught core courses such as Introduction to Translation, Basic and Advanced Interpreting, and Computer-Assisted Translation. 
                    I have served as the principal investigator or main contributor for 12 social science research projects, focusing on translation and educational practices. 
                    I have published 15 peer-reviewed papers and received several teaching awards, including the second prize in the Central China Translation Technology Teaching Competition. 
                    In addition to my academic work, I have provided interpreting services for several international events, including the International Tea Culture Festival and foreign cooperation projects with local governments and universities. 
                    I also review for mutiple international journals.
                </div>"""
    footer = """
                <p class="navbar-text" style="text-align: center;">
                This website followed the design of <a href="https://m-niemeyer.github.io/" target="_blank">Michael Niemeyer</a> and <a href="https://jonbarron.info/" target="_blank">Jon Barron</a>. 
                </p>
    """
    return name, bio_text, social_media, bio, footer

def get_author_dict():
    return {
        'Shuxian Zhang': 'https://www.xyafu.edu.cn/wgyxy/info/1127/7073.htm',
        'Mansour Amini': 'https://ppblt.usm.my/index.php/lecturer-profile/393-mansour-amini-dr',
        'Hualing Gong': 'https://s.wanfangdata.com.cn/paper?q=%E4%BD%9C%E8%80%85%3A%22%E9%BE%9A%E5%8D%8E%E7%8E%B2%22%20%E4%BD%9C%E8%80%85%E5%8D%95%E4%BD%8D%3A%20%22%E4%BF%A1%E9%98%B3%E5%86%9C%E6%9E%97%E5%AD%A6%E9%99%A2%22',
        'Qiongqiong Fan': 'https://www.xyafu.edu.cn/wgyxy/info/1127/7062.htm',
        'Junyue Wang': 'https://www.xyafu.edu.cn/wgyxy/info/1127/7079.htm',
        'Shaidatul Kasuma': 'https://ppblt.usm.my/index.php/lecturer-profile/188-shaidatul-akma-adi-kasuma',
        'Chenjin Jia': 'https://scholar.google.com/citations?hl=en&user=Nk-Ar0IAAAAJ'
        }

def generate_person_html(persons, connection=", ", make_bold=True, make_bold_name='Kashyap Chitta', 
                         add_links=True, equal_contribution=None):
    links = get_author_dict() if add_links else {}
    s = ""

    equal_contributors = -1
    if equal_contribution is not None:
        equal_contributors = equal_contribution
    for idx, p in enumerate(persons):
        string_part_i = ""
        for name_part_i in p.get_part('first') + p.get_part('last'): 
            if string_part_i != "":
                string_part_i += " "
            string_part_i += name_part_i
        if string_part_i in links.keys():
            string_part_i = f'<a href="{links[string_part_i]}" target="_blank">{string_part_i}</a>'
        if make_bold and string_part_i == make_bold_name:
            string_part_i = f'<span style="font-weight: bold";>{make_bold_name}</span>'
        if idx < equal_contributors:
            string_part_i += "*"
        if p != persons[-1]:
            string_part_i += connection
        s += string_part_i
    return s

def get_paper_entry(entry_key, entry):
    if 'highlight' in entry.fields.keys():
        s = """<div style="background-color: #ffffd0; margin-bottom: 3em; padding: 15px"> <div class="row"><div class="col-sm-3 col-4">"""
    else:
        s = """<div style="margin-bottom: 3em;"> <div class="row"><div class="col-md-3 col-4">"""

    s += f"""<img src="{entry.fields['img']}" class="img-fluid img-thumbnail" alt="Project image">"""
    s += """</div><div class="col-md-9 col-8">"""

    if 'award' in entry.fields.keys():
        s += f"""<a href="{entry.fields['html']}" target="_blank" style="font-weight: bold;">{entry.fields['title']}</a> <span style="color: red;">({entry.fields['award']})</span><br>"""
    else:
        s += f"""<a href="{entry.fields['html']}" target="_blank" style="font-weight: bold;">{entry.fields['title']}</a> <br>"""

    if 'equal_contribution' in entry.fields.keys():
        s += f"""{generate_person_html(entry.persons['author'], equal_contribution=int(entry.fields['equal_contribution']))} <br>"""
    else: 
        s += f"""{generate_person_html(entry.persons['author'])} <br>"""
    
    s += f"""<span style="font-style: italic;">{entry.fields['booktitle']}</span>, {entry.fields['year']} <br>"""

    artefacts = {'html': 'Web view', 'pdf': 'Self-archieved Paper', 'supp': 'Supplementary', 'video': 'Video', 'poster': 'Poster', 'code': 'Code'}
    i = 0
    for (k, v) in artefacts.items():
        if k in entry.fields.keys():
            if i > 0:
                s += ' / '
            s += f"""<a href="{entry.fields[k]}" target="_blank">{v}</a>"""
            i += 1
        else:
            print(f'[{entry_key}] Warning: Field {k} missing!')
    
    cite = "<pre><code>@" + entry.type + "{" + f"{entry_key}, \n"
    cite += "\tauthor = {" + f"{generate_person_html(entry.persons['author'], make_bold=False, add_links=False, connection=' and ')}" + "}, \n"
    for entr in ['title', 'booktitle', 'year']:
        cite += f"\t{entr} = " + "{" + f"{entry.fields[entr]}" + "}, \n"
    cite += """}</pre></code>"""
    s += " /" + f"""<button class="btn btn-link" type="button" data-toggle="collapse" data-target="#collapse{entry_key}" aria-expanded="false" aria-controls="collapseExample" style="margin-left: 2px; margin-top: -2px;">Bibtex</button><div class="collapse" id="collapse{entry_key}"><div class="card card-body">{cite}</div></div>"""
    s += """ </div> </div> </div>"""
    return s

def get_talk_entry(entry_key, entry):
    s = """<div style="margin-bottom: 3em;"> <div class="row"><div class="col-sm-3 col-4">"""
    s += f"""<img src="{entry.fields['img']}" class="img-fluid img-thumbnail" alt="Project image">"""
    s += """</div><div class="col-sm-9 col-8">"""   
    s += f"""<span style="font-weight: bold;">{entry.fields['title']}</span><br>"""
    s += f"""<span style="font-style: italic;">{entry.fields['booktitle']}</span>, {entry.fields['year']} <br>"""

    artefacts = {'slides': 'Slides', 'video': 'Recording'}
    i = 0
    for (k, v) in artefacts.items():
        if k in entry.fields.keys():
            if i > 0:
                s += ' / '
            s += f"""<a href="{entry.fields[k]}" target="_blank">{v}</a>"""
            i += 1
        else:
            print(f'[{entry_key}] Warning: Field {k} missing!')
    s += """ </div> </div> </div>"""
    return s

def get_publications_html():
    parser = bibtex.Parser()
    bib_data = parser.parse_file('publication_list.bib')
    keys = bib_data.entries.keys()
    s = ""
    for k in keys:
        s+= get_paper_entry(k, bib_data.entries[k])
    return s

def get_talks_html():
    parser = bibtex.Parser()
    bib_data = parser.parse_file('talk_list.bib')
    keys = bib_data.entries.keys()
    s = ""
    for k in keys:
        s+= get_talk_entry(k, bib_data.entries[k])
    return s

def get_index_html():
    pub = get_publications_html()
    talks = get_talks_html()
    name, bio_text, social_media, bio, footer = get_personal_data()
    s = f"""
    <!doctype html>
<html lang="en">

<head>
  <!-- Required meta tags -->
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <!-- Bootstrap CSS -->
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
    integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    <link rel="stylesheet" <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" integrity="sha512-DTOQO9RWCH3ppGqcWaEA1BIZOC6xxalwEsw9c2QQeAIftl+Vegovlnee1c9QX4TctnWMn13TZye+giMm8e2LwA==" crossorigin="anonymous" referrerpolicy="no-referrer" />

  <title>{name[0] + ' ' + name[1] + ' | Assessment and AI Researcher'}</title>
  <link rel="icon" type="image/x-icon" href="assets/favicon.ico">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&display=swap" rel="stylesheet">
  <link href="https://fonts.googleapis.com/css2?family=Bitter:ital,wght@0,100..900;1,100..900&family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&display=swap" rel="stylesheet">
  <link rel="stylesheet" type="text/css" href="assets/stylesheet.css">
  

</head>

<body>
    <div class="container">
        <div class="row" style="margin-top: 3em;">
            <div class="col-sm-12" style="margin-bottom: 1em;">
            <h3 class="display-4" style="text-align: center;"><span style="font-weight: bold;">{name[0]}</span> {name[1]}</h3>
            </div>
            <br>
            <div class="col-md-10 col-8" style="">
                {bio_text}
            </div>
            <div class="col-md-2 col-4" style="">
                <img src="assets/img/profile.jpg" class="img-thumbnail" alt="Profile picture">
            </div>
            <div class="col-sm-12 align-middle" style="margin-bottom: 1em;">
                {social_media}
                {bio}
            </div>
            
        </div>
        <div class="row" style="margin-top: 3em;">
            <div class="col-sm-12" style="">
                <h4>Publications</h4>
                <p>
                    <span style="font-style: italic; font-size:14px;"> <sup>*</sup>Representative papers are <span style="background-color:#ffffd0">highlighted</span> below.</span>
                </p>
                <hr>
                {pub}
            </div>
        </div>
         <div class="row" style="margin-top: 3em;">
            <div class="col-sm-12" style="">
                <h4>Conferences</h4>
                <hr>
                {talks}
            </div>
        </div>
        <div class="d-flex justify-content-center" style="margin-top: 3em;">
            {footer}
        </div>
    </div>

    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js"
      integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN"
      crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"
      integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q"
      crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"
      integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl"
      crossorigin="anonymous"></script>
</body>

</html>
    """
    return s


def write_index_html(filename='index.html'):
    s = get_index_html()
    with open(filename, 'w',encoding='utf-8') as f:
        f.write(s)
    print(f'Written index content to {filename}.')

if __name__ == '__main__':
    write_index_html('index.html')