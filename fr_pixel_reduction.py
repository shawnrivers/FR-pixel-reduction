import math

# Ideal settings
width = 0.6  # display width
height = 0.35  # display height
distance = 0.5  # distance from user to display
full_resolution_angle = 6  # angle (in deg) for full resolution rendering
half_resolution_angle = 12  # angle (in deg) for half resolution rendering

# Gaze estimation error settings
error = 1  # error angle (in deg) of gaze estimation algorithm
eye_movement_velocity = 100  # slow eye movement velocity (in deg/s)
sampling_rate = 30  # camera sampling rate (in hz)


def toRad(degree):
    return degree * math.pi / 180


def foveatedRenderingRadius(angle, distance):
    return 2 * distance * math.tan(toRad(angle) / 2)


def latency(eye_movement_velocity, sample_rate):
    return eye_movement_velocity * 1 / sample_rate


def pixelReduction(width, height, distance, full_region_angle, half_region_angle):
    display_region = width * height

    full_region_radius = foveatedRenderingRadius(full_region_angle, distance)
    half_region_radius = foveatedRenderingRadius(half_region_angle, distance)

    # Full resolution region
    full_region = math.pi * (full_region_radius ** 2)

    # 60% resolution region
    half_region = math.pi * ((half_region_radius) **
                             2 - (full_region_radius ** 2))

    # 20% resolution region
    rest_region = display_region - half_region

    reduction_ratio = 1 - (full_region + 0.6 * half_region +
                           0.2 * rest_region) / display_region

    return reduction_ratio


def saccadePixelReduction(width, height, distance, full_region_angle, half_region_angle):
    display_region = width * height

    full_region_radius = foveatedRenderingRadius(full_region_angle, distance)
    half_region_radius = foveatedRenderingRadius(half_region_angle, distance)

    # Full resolution region
    full_region = full_region_radius * width

    # 60% resolution region
    half_region = (half_region_radius - full_region_radius) * width

    # 20% resolution region
    rest_region = display_region - half_region

    reduction_ratio = 1 - (full_region + 0.6 * half_region +
                           0.2 * rest_region) / display_region

    return reduction_ratio

# Ideal reduction
ideal_reduction = pixelReduction(
    width, height, distance, full_resolution_angle, half_resolution_angle)
ideal_reduction_saccade = saccadePixelReduction(
    width, height, distance, full_resolution_angle, half_resolution_angle)

# Reduction with spatial error considered
fra_with_spatial_error = full_resolution_angle + error
hra_with_spatial_error = half_resolution_angle + error

spatial_error_reduction = pixelReduction(
    width, height, distance,
    fra_with_spatial_error,
    hra_with_spatial_error)
spatial_error_reduction_saccade = saccadePixelReduction(
    width, height, distance,
    fra_with_spatial_error,
    hra_with_spatial_error)

# Reduction with latency considered
fra_with_latency = full_resolution_angle + \
    latency(eye_movement_velocity, sampling_rate)
hra_with_latency = half_resolution_angle + \
    latency(eye_movement_velocity, sampling_rate)

latency_reduction = pixelReduction(
    width, height, distance,
    fra_with_latency,
    hra_with_latency)
latency_reduction_saccade = saccadePixelReduction(
    width, height, distance,
    fra_with_latency,
    hra_with_latency)

# Reduction with both spatial and latency considered
fra_real = full_resolution_angle + error + \
    latency(eye_movement_velocity, sampling_rate)
hra_real = half_resolution_angle + error + \
    latency(eye_movement_velocity, sampling_rate)

real_reduction = pixelReduction(width, height, distance, fra_real, hra_real)
real_reduction_saccade = saccadePixelReduction(width, height, distance, fra_real, hra_real)

print("\nIdeal reduction rate:\n  Normal: %2.2f%%\n  Saccade: %2.2f%%" % ((ideal_reduction) * 100, (ideal_reduction_saccade) * 100))
print("Reduction rate (with %1d deg spatial error):\n  Normal: %2.2f%%\n  Saccade: %2.2f%%" %
      (error, (spatial_error_reduction) * 100, (spatial_error_reduction_saccade) * 100))
print("Reduction rate (using %2d Hz camera):\n  Normal: %2.2f-%2.2f%%\n  Saccade: %2.2f-%2.2f%%" %
      (sampling_rate, (ideal_reduction) * 100, (latency_reduction) * 100, (ideal_reduction_saccade) * 100, (latency_reduction_saccade) * 100))
print("Real reduction rate:\n  Normal: %2.2f-%2.2f%%\n  Saccade: %2.2f-%2.2f%%" %
      ((spatial_error_reduction) * 100, (real_reduction) * 100, (spatial_error_reduction_saccade) * 100, (real_reduction_saccade) * 100))


# max_saccade_angle = 2 * math.atan(((width ** 2 + height ** 2) ** 0.5) / (2 * distance))
# print("Max saccade angle: %4.2f rad (%5.2f deg)" % (max_saccade_angle, max_saccade_angle * 180 / math.pi))
