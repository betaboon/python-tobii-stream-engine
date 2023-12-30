
tobii_error_t tobii_gaze_data_subscribe( tobii_device_t* device,
    tobii_gaze_data_callback_t callback, void* user_data );

tobii_error_t tobii_gaze_data_unsubscribe( tobii_device_t* device );

tobii_error_t tobii_digital_syncport_subscribe( tobii_device_t* device,
    tobii_digital_syncport_callback_t callback, void* user_data );

tobii_error_t tobii_digital_syncport_unsubscribe( tobii_device_t* device );

tobii_error_t tobii_enumerate_face_types( tobii_device_t* device, tobii_face_type_receiver_t receiver,
  void* user_data );

tobii_error_t tobii_set_face_type( tobii_device_t* device, tobii_face_type_t const face_type );

tobii_error_t tobii_get_face_type( tobii_device_t* device, tobii_face_type_t* face_type );
