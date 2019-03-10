import subprocess
import random
import os
import time
import shutil
import json


TOTAL_NUM_OF_BUGS = 8
NUM_OF_MUTATION = 10000
WORKING_DIR = os.getcwd()
MOMENT=time.strftime("%Y-%b-%d__%H_%M_%S",time.localtime())
DESTINATION = os.path.join(WORKING_DIR, "archive", "run_{}".format(MOMENT))

def findbugnumber(text):
    text_list = text.split(" ")
    bug_num = text_list[1][1]
    return bug_num

def read_image_as_byte_array(input_file):
    with open(input_file, "rb") as file:
        content = list(file.read())
        buffer = bytearray(content)
        return buffer

def mutate_byte_array(buffer, num):
    mutation_method = num %3
    # mutation_method = 0
    if mutation_method == 0: #change one byte at a random location to a random value
        buff_len = len(buffer)
        rand_pos = random.randint(0, buff_len - 1)
        buffer[rand_pos] = random.randint(0, 255)
        return buffer

    elif mutation_method == 1: #change m consecutive bytes at a random location to all zeros
        buff_len = len(buffer)
        rand_pos = random.randint(0, buff_len - 1)
        m = random.randint(3,int(buff_len/2))
        for i in range(1,m):
            if (rand_pos+i) >= buff_len:
                rand_pos = 0
            buffer[rand_pos+i] = 0
        return buffer

    elif mutation_method == 2: #change m consecutive bytes at a random location to 255
        buff_len = len(buffer)
        rand_pos = random.randint(0, buff_len - 1)
        m = random.randint(3, int(buff_len/2))
        for i in range(1,m):
            if (rand_pos+i) >= buff_len:
                rand_pos = 0
            buffer[rand_pos+i] = 255
        return buffer



def save_byte_array_as_image(byte_array, output_file):
    with open(output_file, "wb") as file:
        file.write(byte_array)

def run_target_program(input_file, output_file):
    cmd = ["./jpg2bmp", input_file, output_file]
    test = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    output, stderr = test.communicate()
    return output

def remove_file(file):
    file_to_remove = os.path.join(WORKING_DIR, file)
    if os.path.isfile(file_to_remove):
        # print("Removing file: ", file_to_remove)
        os.remove(file_to_remove)

def save_report(report):
    report_file_name = os.path.join(DESTINATION, "report.json")
    with open(report_file_name, "wb") as file:
        file.write(json.dumps(report, indent=4))

def archive_test_files():
    if not os.path.isdir("archive"):
        os.mkdir("archive")
    os.makedirs(DESTINATION)
    files = os.listdir(WORKING_DIR)
    for file in files:
        if ("test" in file) and (".jpg" in file):
            src = os.path.join(WORKING_DIR, file)
            dst = os.path.join(DESTINATION, file)
            shutil.move(src, dst)
    print("All test Files which produceed bugs moved to archive: {}".format(DESTINATION))

def main():
    BUGS_FOUND = []
    count_bug1 = 0
    count_bug2 = 0
    count_bug3 = 0
    count_bug4 = 0
    count_bug5 = 0
    count_bug6 = 0
    count_bug7 = 0
    count_bug8 = 0



    for i in range(NUM_OF_MUTATION):
        buffer = read_image_as_byte_array("cross.jpg")
        buffer_mutated = mutate_byte_array(buffer, i)
        file_name = "test{}.jpg".format(i)
        save_byte_array_as_image(buffer_mutated, file_name)

        input_file = file_name
        output_file = "test{}.bmp".format(i)
        output = run_target_program(input_file, output_file)

        if 'Bug' not in output:
            remove_file(input_file)
            remove_file(output_file)

        elif 'Bug' in output:
            bug_num = findbugnumber(output)
            if bug_num == '1':
                count_bug1 += 1
            if bug_num == '2':
                count_bug2 += 1
            if bug_num == '3':
                count_bug3 += 1
            if bug_num == '4':
                count_bug4 += 1
            if bug_num == '5':
                count_bug5 += 1
            if bug_num == '6':
                count_bug6 += 1
            if bug_num == '7':
                count_bug7 += 1
            if bug_num == '8':
                count_bug8 += 1

            new_file_name = input_file.split('.')[0] + "_bug_{}.jpg".format(bug_num)
            os.rename(input_file, new_file_name)
            print(output + "Bug Triggered by {0}, renamed to {1}".format(input_file, new_file_name))

            if bug_num not in BUGS_FOUND:
                BUGS_FOUND.append(bug_num)
            elif len(BUGS_FOUND)==TOTAL_NUM_OF_BUGS:
                print("All {} bugs found, exiting program".format(TOTAL_NUM_OF_BUGS))
                break

        else:
            print("This shouldn't print", output)

        if i%1000 == 0:
            print("\n****************Iteration {0}. Bugs found: {1}*******************\n".format(i,BUGS_FOUND))



        # remove_test.remove()


    total_bugs_trigerred = count_bug1 + count_bug2 + count_bug3 + count_bug4 + count_bug5 + count_bug6 + count_bug7 + count_bug8
    print("*******REPORT*******")
    print("Number of test_files: {}".format(i+1))
    print("Bugs Trigerred: {} times".format(total_bugs_trigerred))
    print("Bug1_count: {}".format(count_bug1))
    print("Bug2_count: {}".format(count_bug2))
    print("Bug3_count: {}".format(count_bug3))
    print("Bug4_count: {}".format(count_bug4))
    print("Bug5_count: {}".format(count_bug5))
    print("Bug6_count: {}".format(count_bug6))
    print("Bug7_count: {}".format(count_bug7))
    print("Bug8_count: {}".format(count_bug8))

    report = {
        "num_of_test_files": i+1,
        "num_of_bugs_trigerred": total_bugs_trigerred,
        "bug1_count": count_bug1,
        "bug2_count": count_bug2,
        "bug3_count": count_bug3,
        "bug4_count": count_bug4,
        "bug5_count": count_bug5,
        "bug6_count": count_bug6,
        "bug7_count": count_bug7,
        "bug8_count": count_bug8,
    }

    if len(BUGS_FOUND) !=0:
        archive_test_files()
        save_report(report)

if __name__ == '__main__':
    main()
