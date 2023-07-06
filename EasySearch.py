import requests
import bs4
import linkedin_api

def get_linkedin_data(linkedin_url, salary, benefits, years_of_experience):
  """Returns a dictionary of data from the LinkedIn URL."""

  response = requests.get(linkedin_url)
  soup = bs4.BeautifulSoup(response.content, "html.parser")

  data = {}

  # Get personal contact information.

  data["first_name"] = soup.find("span", class_="full-name").text.split(" ")[0]
  data["last_name"] = soup.find("span", class_="full-name").text.split(" ")[1]
  data["phone_number"] = soup.find("li", class_="pv-contact-info__phone").text
  data["email"] = soup.find("li", class_="pv-contact-info__email").text
  data["address"] = soup.find("li", class_="pv-contact-info__address").text

  # Get professional summary.

  data["professional_summary"] = soup.find("div", class_="summary").text

  # Get core competencies.

  data["core_competencies"] = [
      skill.text for skill in soup.find_all("li", class_="pv-skills-section__skill-item")
  ]

  # Get education.

  data["education"] = []
  for education_item in soup.find_all("div", class_="pv-education-summary__item"):
    school = education_item.find("h3", class_="pv-education-summary__school").text
    degree = education_item.find("h4", class_="pv-education-summary__degree").text
    concentration = education_item.find("span", class_="pv-education-summary__field-of-study").text
    year_graduated = education_item.find("span", class_="pv-education-summary__year").text
    data["education"].append({
        "school": school,
        "degree": degree,
        "concentration": concentration,
        "year_graduated": year_graduated,
    })

  # Get work experience.

  data["work_experience"] = []
  for work_experience_item in soup.find_all("div", class_="pv-work-experience-entity"):
    employer = work_experience_item.find("h3", class_="pv-work-experience-entity__company").text
    position = work_experience_item.find("h4", class_="pv-work-experience-entity__position").text
    length_at_company = work_experience_item.find("span", class_="pv-work-experience-entity__dates").text
    work_experience = work_experience_item.find("div", class_="pv-work-experience-entity__description").text
    data["work_experience"].append({
        "employer": employer,
        "position": position,
        "length_at_company": length_at_company,
        "work_experience": work_experience,
    })

  # Set job query controls.

  data["salary"] = salary
  data["benefits"] = benefits
  data["years_of_experience"] = years_of_experience

  # Use AI/ML to find "easy apply jobs" on LinkedIn.

  jobs = linkedin_api.find_easy_apply_jobs(data)

  return data, jobs


if __name__ == "__main__":
  linkedin_url = "https://www.linkedin.com/in/johndoe/"
  salary = 100000
  benefits = "Health insurance, dental insurance, vision insurance, 401k, paid time off"
  years_of_experience = 5
  data, jobs = get_linkedin_data(linkedin_url, salary, benefits, years_of_experience)
  print(data)
  print(jobs)
