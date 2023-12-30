
tobii_error_t tobii_gaze_point_subscribe( tobii_device_t* device,
    tobii_gaze_point_callback_t callback, void* user_data );

tobii_error_t tobii_gaze_point_unsubscribe( tobii_device_t* device );

tobii_error_t tobii_gaze_origin_subscribe( tobii_device_t* device,
    tobii_gaze_origin_callback_t callback, void* user_data );

tobii_error_t tobii_gaze_origin_unsubscribe( tobii_device_t* device );

tobii_error_t tobii_eye_position_normalized_subscribe( tobii_device_t* device,
    tobii_eye_position_normalized_callback_t callback, void* user_data );

tobii_error_t tobii_eye_position_normalized_unsubscribe( 
    tobii_device_t* device );

tobii_error_t tobii_user_presence_subscribe( tobii_device_t* device,
    tobii_user_presence_callback_t callback, void* user_data );

tobii_error_t tobii_user_presence_unsubscribe( tobii_device_t* device );

tobii_error_t tobii_head_pose_subscribe( tobii_device_t* device,
    tobii_head_pose_callback_t callback, void* user_data );

tobii_error_t tobii_head_pose_unsubscribe( tobii_device_t* device );

tobii_error_t tobii_notifications_subscribe( tobii_device_t* device,
    tobii_notifications_callback_t callback, void* user_data );

tobii_error_t tobii_notifications_unsubscribe( tobii_device_t* device );

tobii_error_t tobii_user_position_guide_subscribe( tobii_device_t* device,
    tobii_user_position_guide_callback_t callback, void* user_data );

tobii_error_t tobii_user_position_guide_unsubscribe( tobii_device_t* device );
