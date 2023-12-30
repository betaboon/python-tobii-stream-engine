
char const* tobii_error_message( tobii_error_t error );

tobii_error_t tobii_get_api_version( tobii_version_t* version );

tobii_error_t tobii_api_create( tobii_api_t** api,
    tobii_custom_alloc_t const* custom_alloc, tobii_custom_log_t const* custom_log );

tobii_error_t tobii_api_destroy( tobii_api_t* api );

tobii_error_t tobii_enumerate_local_device_urls( tobii_api_t* api,
    tobii_device_url_receiver_t receiver, void* user_data );

tobii_error_t tobii_enumerate_local_device_urls_ex( tobii_api_t* api,
    tobii_device_url_receiver_t receiver, void* user_data,
    uint32_t device_generations );

tobii_error_t tobii_device_create( tobii_api_t* api, char const* url,
    tobii_field_of_use_t field_of_use, tobii_device_t** device );

tobii_error_t tobii_device_destroy( tobii_device_t* device );

tobii_error_t tobii_wait_for_callbacks( int device_count, tobii_device_t* const* devices );

tobii_error_t tobii_device_process_callbacks( tobii_device_t* device );

tobii_error_t tobii_device_clear_callback_buffers( tobii_device_t* device );

tobii_error_t tobii_device_reconnect( tobii_device_t* device );

tobii_error_t tobii_update_timesync( tobii_device_t* device );

tobii_error_t tobii_system_clock( tobii_api_t* api, int64_t* timestamp_us );

tobii_error_t tobii_get_device_info( tobii_device_t* device,
    tobii_device_info_t* device_info );

tobii_error_t tobii_get_track_box( tobii_device_t* device, tobii_track_box_t* track_box );

tobii_error_t tobii_get_state_bool( tobii_device_t* device, tobii_state_t state,
    tobii_state_bool_t* value );

tobii_error_t tobii_get_state_uint32( tobii_device_t* device, tobii_state_t state,
    uint32_t* value );

tobii_error_t tobii_get_state_string( tobii_device_t* device, tobii_state_t state,
    tobii_state_string_t value );

tobii_error_t tobii_capability_supported( tobii_device_t* device,
    tobii_capability_t capability, tobii_supported_t* supported );

tobii_error_t tobii_stream_supported( tobii_device_t* device,
    tobii_stream_t stream, tobii_supported_t* supported );
