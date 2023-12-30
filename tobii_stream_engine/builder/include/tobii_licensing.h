
tobii_error_t tobii_device_create_ex( tobii_api_t* api, char const* url, tobii_field_of_use_t field_of_use,
    tobii_license_key_t const* license_keys, int license_count, tobii_license_validation_result_t* license_results, tobii_device_t** device );

tobii_error_t tobii_license_key_store( tobii_device_t* device, void* data, size_t size );

tobii_error_t tobii_license_key_retrieve( tobii_device_t* device, tobii_data_receiver_t receiver, void* user_data );

tobii_error_t tobii_get_feature_group( tobii_device_t* device, tobii_feature_group_t* feature_group );
