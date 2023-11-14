from scipy import stats
import numpy as np
import pylab
import csv


def read_OD(row_number):
    # Read OD_value form csv file in the same folder
    OD_value = []
    with open('sample.csv', 'r', newline='') as csvfile:
        spamreader = csv.DictReader(csvfile, dialect='excel')
        for row in spamreader:
            if row[row_number] != "":
                OD_value.append(float(row[row_number]))
    return OD_value


# Get the reading OD value of standards and samples.
concentration = [0.0, 0.1, 0.2, 0.5, 1.0, 1.5, 2.0]   # mg/ml
standard_1 = read_OD(str(1))  # OD value
standard_2 = read_OD(str(2))  # OD value


# Calculate average OD value of standards
standard_AVG = []
for i in range(len(concentration)):
    standard_AVG.append(round((standard_1[i] + standard_2[i]) / 2, 4))
print("standard_AVG is: ", end="")
print(standard_AVG)

# Calculate sample OD value
sample_OD_1 = read_OD(str(3))
sample_OD_2 = read_OD(str(4))
sample_OD_3 = read_OD(str(5))
sample_AVG = []
for i in range(len(sample_OD_1)):
    sample_AVG.append(
        round((sample_OD_1[i] + sample_OD_2[i] + sample_OD_3[i]) / 3, 4))
print("sample_AVG is: ", end="")
print(sample_AVG)


# Make the standard curve. Get regression of OD value and concentrations.
x = np.array(concentration)
y = np.array(standard_AVG)
slope, intercept, r_value, p_value, slope_std_error = stats.linregress(x, y)

# Calculate some additional outputs
predict_y = intercept + slope * x
pred_error = y - predict_y
degrees_of_freedom = len(x) - 2
residual_std_error = np.sqrt(np.sum(pred_error ** 2) / degrees_of_freedom)

# Plotting. Get the standard curve and R**2.
pylab.plot(x, y, 'o')
pylab.plot(x, predict_y, 'k-')
pylab.show()
R2 = "R2 = " + str(r_value ** 2)
print(R2)
equation = "y = " + str(slope) + "x + " + str(intercept)
print(equation)


# Calculate sample concentrations.
sample_vol = 3  # ul
total_vol = 30  # ul
load_protein = 100  # ug, amount of protein load in gel
well_vol = 100  # ul, gel well volume


# Calculate sample concentration.
sample_concentration = []
for i in sample_AVG:
    sample_concentration.append(
        round((i - intercept) / slope * total_vol / sample_vol, 2))  # mg/ml
print("sample_concentration is: ", end="")
print(sample_concentration)

# Calculate dilution samples: with Nupage gel, reducing buffer, LDS buffer
# and water.
dilution_vol = []
MQ_H2O = []
LDS_buffer = []
reducing_buffer = []
for i in sample_concentration:
    sample = round(load_protein / i, 1)  # ul
    LDS = well_vol / 4  # ul
    reducing = well_vol / 10  # ul
    H2O = well_vol - sample - LDS - reducing  # ul
    dilution_vol.append(sample)
    MQ_H2O.append(H2O)
    LDS_buffer.append(LDS)
    reducing_buffer.append(reducing)
# print("dilution_vol is: ", end="")
# print(dilution_vol)
# print("MQ_H2O is: ", end="")
# print(MQ_H2O)
# print("LDS_buffer is: ", end="")
# print(LDS_buffer)
# print("reducing_buffer is: ", end="")
# print(reducing_buffer)





with open('BCA results and calculation.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, dialect='excel')
    spamwriter.writerow(['', 'sample name', 'sample name', 'sample name',
                         'sample name', 'sample name', 'sample name', 'sample name', 'sample name'])
    spamwriter.writerow(
        ['sample_concentration'] + [x for x in sample_concentration] + ["ug/ul"])
    spamwriter.writerow([])
    spamwriter.writerow([])
    spamwriter.writerow(['', 'sample name', 'sample name', 'sample name',
                         'sample name', 'sample name', 'sample name', 'sample name', 'sample name'])
    spamwriter.writerow(['dilution vol'] + [x for x in dilution_vol] + ['ul'])
    spamwriter.writerow(
        ['reducing buffer'] + [x for x in reducing_buffer] + ['ul'])
    spamwriter.writerow(['LDS buffer'] + [x for x in LDS_buffer] + ['ul'])
    spamwriter.writerow(['MQ H2O'] + [x for x in MQ_H2O] + ['ul'])
    spamwriter.writerow([])
    spamwriter.writerow([])
    spamwriter.writerow(
        ['Amount of protein per well:'] + [load_protein] + ['ug'])
    spamwriter.writerow(['Well volume:'] + [well_vol] + ['ug'])
    spamwriter.writerow([])
    spamwriter.writerow([equation] + [R2])
