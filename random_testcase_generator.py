import csv
import random
# ___________________________________________________________Generates Random Test Cases(As per assumptions)_______________________________________________________________
# makes a input.csv file by editing line 73,74,75,76 with required inputs
def generate_input(
    num_faculty, num_courses, num_elec_courses, num_hdcdc_courses
):
    input = []
    all_cdc = set()
    all_electives = set()
    all_hd_cdc = set()
    all_hd_elec = set()

    for i in range(1, num_faculty + 1):
        if i < 0.4 * num_faculty:
            max_load = 3
        else:
            max_load = 2

        # Ensure each course appears exactly once in course_pref
        course_pref = random.sample(range(1, num_courses + 1), 4)
        all_cdc.update(course_pref)
        course_pref = "[" + " ".join(map(str, course_pref)) + "]"

        # Ensure each elective course appears exactly once in elec_pref
        elec_pref_courses = list(range(1, num_elec_courses + 1))
        elec_pref = random.sample(elec_pref_courses, 4)
        all_electives.update(elec_pref)
        elec_pref = "[" + " ".join(map(str, elec_pref)) + "]"

        # Generate unique Hd CDC preferences for each faculty member with a size of 2
        hd_cdc_courses = list(range(1, num_hdcdc_courses + 1))
        hd_cdc_pref = random.sample(hd_cdc_courses, 2)
        all_hd_cdc.update(hd_cdc_pref)
        hd_cdc_pref = "[" + " ".join(map(str, hd_cdc_pref)) + "]"

        # Generate unique Hd Elec preferences for each faculty member with a size of 2
        hd_elec_courses = list(range(1, num_hd_ele + 1))
        hd_elec_pref = random.sample(hd_elec_courses, 2)
        all_hd_elec.update(hd_elec_pref)
        hd_elec_pref = "[" + " ".join(map(str, hd_elec_pref)) + "]"

        faculty_name = f"Professor_{i}"
        input.append(
            [
                faculty_name,
                i,
                max_load,
                course_pref,
                elec_pref,
                hd_cdc_pref,
                hd_elec_pref,
            ]
        )

    return (
        input,
        list(all_cdc),
        list(all_electives),
        list(all_hd_cdc),
        list(all_hd_elec),
    )


def write_to_csv(filename, header, data):
    with open(filename, "w", newline="") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(header)
        csv_writer.writerows(data)


if __name__ == "__main__":
    num_faculty = 30  # no of faculties
    num_courses = 11  # no of FD cdc
    num_elec_courses = 7  # no of FD electives
    num_hdcdc_courses = 10  # no of HD cdc
    num_hd_ele = 7  # no of HD elec
    header = [
        "Faculty_Name",
        "Faculty_Num",
        "Max_Load",
        "Course_Pref",
        "Elec_Pref",
        "Hd_CDC_Pref",
        "Hd_Elec_Pref",
    ]

    (
        input,
        all_cdc,
        all_electives,
        all_hd_cdc,
        all_hd_elec,
    ) = generate_input(
        num_faculty, num_courses, num_elec_courses, num_hdcdc_courses
    )

    write_to_csv("input.csv", header, input)

    # Output the lists of all course preferences (CDC), all elective preferences, Hd CDC preferences, and Hd Elec preferences
    if sum(all_cdc) != num_courses * (num_courses + 1) / 2:
        print("Something wrong in CDC generation")
    else:
        print("CDC's correct generation")
    if sum(all_electives) != num_elec_courses * (num_elec_courses + 1) / 2:
        print("Something wrong in Elec generation")
    else:
        print("Electives correct generation")
    if sum(all_hd_cdc) != num_hdcdc_courses * (num_hdcdc_courses + 1) / 2:
        print("Something wrong in Hd CDC generation")
    else:
        print("Hd CDC's correct generation")
    if sum(all_hd_elec) != num_hd_ele * (num_hd_ele + 1) / 2:
        print("Something wrong in Hd Elec generation")
    else:
        print("Hd Elec's correct generation")
