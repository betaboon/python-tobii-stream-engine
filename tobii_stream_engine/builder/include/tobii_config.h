
tobii_error_t tobii_set_enabled_eye( tobii_device_t* device, tobii_enabled_eye_t enabled_eye );

tobii_error_t tobii_get_enabled_eye( tobii_device_t* device, tobii_enabled_eye_t* enabled_eye );

tobii_error_t tobii_calibration_start( tobii_device_t* device, 
    tobii_enabled_eye_t enabled_eye );

tobii_error_t tobii_calibration_stop( tobii_device_t* device );

tobii_error_t tobii_calibration_collect_data_2d( tobii_device_t* device, 
    float x, float y );

tobii_error_t tobii_calibration_collect_data_3d( tobii_device_t* device, 
    float x, float y, float z );

tobii_error_t tobii_calibration_collect_data_per_eye_2d( tobii_device_t* device, 
    float x, float y, tobii_enabled_eye_t requested_eyes, 
    tobii_enabled_eye_t* collected_eyes );

tobii_error_t tobii_calibration_discard_data_2d( tobii_device_t* device, 
    float x, float y );

tobii_error_t tobii_calibration_discard_data_3d( tobii_device_t* device, 
    float x, float y, float z );

tobii_error_t tobii_calibration_discard_data_per_eye_2d( tobii_device_t* device, 
    float x, float y, tobii_enabled_eye_t eyes );

tobii_error_t tobii_calibration_clear( tobii_device_t* device );

tobii_error_t tobii_calibration_compute_and_apply( tobii_device_t* device );

tobii_error_t tobii_calibration_compute_and_apply_per_eye( tobii_device_t* device, 
    tobii_enabled_eye_t* calibrated_eyes );

tobii_error_t tobii_calibration_retrieve( tobii_device_t* device, 
    tobii_data_receiver_t receiver, void* user_data );

tobii_error_t tobii_calibration_parse( tobii_api_t* api, void const* data, 
    size_t data_size, tobii_calibration_point_data_receiver_t receiver, 
    void* user_data );

tobii_error_t tobii_calibration_apply( tobii_device_t* device, 
    void const* data, size_t size );

tobii_error_t tobii_get_geometry_mounting( tobii_device_t* device, 
    tobii_geometry_mounting_t* geometry_mounting );

tobii_error_t tobii_get_display_area( tobii_device_t* device, 
    tobii_display_area_t* display_area );

tobii_error_t tobii_set_display_area( tobii_device_t* device, 
    tobii_display_area_t const* display_area );

tobii_error_t tobii_calculate_display_area_basic( tobii_api_t* api, 
    float width_mm, float height_mm, float offset_x_mm, 
    tobii_geometry_mounting_t const* geometry_mounting, 
    tobii_display_area_t* display_area );

tobii_error_t tobii_get_device_name( tobii_device_t* device, 
    tobii_device_name_t* device_name );

tobii_error_t tobii_set_device_name( tobii_device_t* device, 
    tobii_device_name_t const device_name );

tobii_error_t tobii_enumerate_output_frequencies( tobii_device_t* device, 
    tobii_output_frequency_receiver_t receiver, void* user_data );

tobii_error_t tobii_set_output_frequency( tobii_device_t* device, 
    float output_frequency );

tobii_error_t tobii_get_output_frequency( tobii_device_t* device, 
    float* output_frequency );
