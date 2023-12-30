
tobii_error_t tobii_wearable_consumer_data_subscribe( tobii_device_t* device,
    tobii_wearable_consumer_data_callback_t callback, void* user_data );

tobii_error_t tobii_wearable_consumer_data_unsubscribe( tobii_device_t* device );

tobii_error_t tobii_wearable_advanced_data_subscribe( tobii_device_t* device,
    tobii_wearable_advanced_data_callback_t callback, void* user_data );

tobii_error_t tobii_wearable_advanced_data_unsubscribe( tobii_device_t* device );

tobii_error_t tobii_get_lens_configuration( tobii_device_t* device,
    tobii_lens_configuration_t* lens_config );

tobii_error_t tobii_set_lens_configuration( tobii_device_t* device,
    tobii_lens_configuration_t const* lens_config );

tobii_error_t tobii_lens_configuration_writable( tobii_device_t* device,
    tobii_lens_configuration_writable_t* writable );

tobii_error_t tobii_wearable_foveated_gaze_subscribe( tobii_device_t* device,
    tobii_wearable_foveated_gaze_callback_t callback, void* user_data );

tobii_error_t tobii_wearable_foveated_gaze_unsubscribe( tobii_device_t* device );
