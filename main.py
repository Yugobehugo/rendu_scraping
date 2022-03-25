import requests
from bs4 import BeautifulSoup
import requests_cache

requests_cache.install_cache('demo_cache')


class statistiques(object):

    def __init__(self, current_url):
        self.url = current_url


    def make_request(self):
        page = requests.get(self.url)
        return page.text

    def make_soup(self):
        return BeautifulSoup(self.make_request(), 'html.parser')

    def data(self, div_id):
        content = self.make_soup().find("div", {"id": div_id})
        title = content.find("div", {"class": "section_heading"}).findChildren("h2")[0].get_text()

        return title, content

    def data_stats(self):
        title, content = self.data("all_stats_standard")

        titles = [title.text for title in content.find("table").find("thead").find_all("tr")[-1].findChildren("th")]
        player_list = content.find("table").find("tbody").findChildren("tr")

        for player in player_list:
            player_name = player.find("th").text
            datas = [data.text for data in player.findChildren("td")]
            datas = [player_name, datas]

            full_data = []
            full_data.append(dict(zip(titles, datas)))

        return title, full_data



    def data_tirs(self):
        title, content = self.data("all_stats_shooting")

        titles = [title.text for title in content.find("table").find("thead").find_all("tr")[-1].findChildren("th")]
        tir_list = content.find("tbody").findChildren("tr")

        for player in tir_list:
            player_name = player.find("th").text
            datas = [data.text for data in player.findChildren("td")]
            datas = [player_name, datas]
            full_data = []
            full_data.append(dict(zip(titles, datas)))

        return title, full_data

    def data_calendar(self):
        title, content = self.data("all_matchlogs")

        titles = [title.text for title in content.find("table").find("thead").find("tr").findChildren("th")]
        calendar_list = content.find("tbody").findChildren("tr")

        for calendar_date in calendar_list:
            date = calendar_date.find("th").text
            datas = [data.text for data in calendar_date.findChildren("td")]
            datas = [date, datas]
            full_data = []
            full_data.append(dict(zip(titles, datas)))

        return title, full_data

    def all_data(self):
        all_data = self.data_stats(), self.data_tirs(), self.data_calendar()
        return list(all_data)


if __name__ == "__main__":
    result = statistiques("https://fbref.com/fr/equipes/361ca564/Statistiques-Tottenham-Hotspur").all_data()
    print(result)
