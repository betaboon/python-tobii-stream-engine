/*
This is derived from:
https://tobiitech.github.io/stream-engine-docs/
*/


// typedefs for tobii.h

typedef enum tobii_error_t
{
    TOBII_ERROR_NO_ERROR,
    TOBII_ERROR_INTERNAL,
    TOBII_ERROR_INSUFFICIENT_LICENSE,
    TOBII_ERROR_NOT_SUPPORTED,
    TOBII_ERROR_NOT_AVAILABLE,
    TOBII_ERROR_CONNECTION_FAILED,
    TOBII_ERROR_TIMED_OUT,
    TOBII_ERROR_ALLOCATION_FAILED,
    TOBII_ERROR_INVALID_PARAMETER,
    TOBII_ERROR_CALIBRATION_ALREADY_STARTED,
    TOBII_ERROR_CALIBRATION_NOT_STARTED,
    TOBII_ERROR_ALREADY_SUBSCRIBED,
    TOBII_ERROR_NOT_SUBSCRIBED,
    TOBII_ERROR_OPERATION_FAILED,
    TOBII_ERROR_CONFLICTING_API_INSTANCES,  // this is not mentioned in the documentation
    TOBII_ERROR_CALIBRATION_BUSY,
    TOBII_ERROR_CALLBACK_IN_PROGRESS,
    TOBII_ERROR_TOO_MANY_SUBSCRIBERS,
    TOBII_ERROR_CONNECTION_FAILED_DRIVER,  // this is not mentioned in the documentation
} tobii_error_t;

typedef struct tobii_version_t
{
    int major;
    int minor;
    int revision;
    int build;
} tobii_version_t;

typedef struct tobii_api_t tobii_api_t;

typedef void* (*tobii_malloc_func_t)( void* mem_context, size_t size );

typedef void (*tobii_free_func_t)( void* mem_context, void* ptr );

typedef struct tobii_custom_alloc_t
{
    void* mem_context;
    tobii_malloc_func_t malloc_func;
    tobii_free_func_t free_func;
} tobii_custom_alloc_t;

typedef enum tobii_log_level_t
{
    TOBII_LOG_LEVEL_ERROR,
    TOBII_LOG_LEVEL_WARN,
    TOBII_LOG_LEVEL_INFO,
    TOBII_LOG_LEVEL_DEBUG,
    TOBII_LOG_LEVEL_TRACE,
} tobii_log_level_t;

typedef void (*tobii_log_func_t)( void* log_context, tobii_log_level_t level, char const* text );

typedef struct tobii_custom_log_t
{
    void* log_context;
    tobii_log_func_t log_func;
} tobii_custom_log_t;

typedef void (*tobii_device_url_receiver_t)( char const* url, void* user_data );

typedef struct tobii_device_t tobii_device_t;

typedef enum tobii_field_of_use_t
{
  TOBII_FIELD_OF_USE_INTERACTIVE = 1,
  TOBII_FIELD_OF_USE_ANALYTICAL = 2,
} tobii_field_of_use_t;

typedef struct tobii_device_info_t
{
    char serial_number[ 256 ];
    char model[ 256 ];
    char generation[ 256 ];
    char firmware_version[ 256 ];
    // v-- these are not mentioned in the documentation
    // they are required tho, taken from old package
    char integration_id[ 128 ];
    char hw_calibration_version[ 128 ];
    char hw_calibration_date[ 128 ];
    char lot_id[ 128 ];
    char integration_type[ 256 ];
    char runtime_build_version[ 256 ];
    // ^--
} tobii_device_info_t;

typedef struct tobii_track_box_t
{
    float front_upper_right_xyz[ 3 ];
    float front_upper_left_xyz[ 3 ];
    float front_lower_left_xyz[ 3 ];
    float front_lower_right_xyz[ 3 ];
    float back_upper_right_xyz[ 3 ];
    float back_upper_left_xyz[ 3 ];
    float back_lower_left_xyz[ 3 ];
    float back_lower_right_xyz[ 3 ];
} tobii_track_box_t;

typedef enum tobii_state_t
{
    TOBII_STATE_POWER_SAVE_ACTIVE,
    TOBII_STATE_REMOTE_WAKE_ACTIVE,
    TOBII_STATE_DEVICE_PAUSED,
    TOBII_STATE_EXCLUSIVE_MODE,
    TOBII_STATE_FAULT,
    TOBII_STATE_WARNING,
    TOBII_STATE_CALIBRATION_ID,
    TOBII_STATE_CALIBRATION_ACTIVE,  // this is not mentioned in the documentation
} tobii_state_t;

typedef enum tobii_state_bool_t
{
    TOBII_STATE_BOOL_FALSE,
    TOBII_STATE_BOOL_TRUE,
} tobii_state_bool_t;

typedef char tobii_state_string_t[512];

typedef enum tobii_capability_t
{
    TOBII_CAPABILITY_DISPLAY_AREA_WRITABLE,
    TOBII_CAPABILITY_CALIBRATION_2D,
    TOBII_CAPABILITY_CALIBRATION_3D,
    TOBII_CAPABILITY_PERSISTENT_STORAGE,
    TOBII_CAPABILITY_CALIBRATION_PER_EYE,
    TOBII_CAPABILITY_COMPOUND_STREAM_WEARABLE_3D_GAZE_COMBINED,
    TOBII_CAPABILITY_FACE_TYPE,
    TOBII_CAPABILITY_COMPOUND_STREAM_USER_POSITION_GUIDE_XY,
    TOBII_CAPABILITY_COMPOUND_STREAM_USER_POSITION_GUIDE_Z,
    TOBII_CAPABILITY_COMPOUND_STREAM_WEARABLE_LIMITED_IMAGE,
    TOBII_CAPABILITY_COMPOUND_STREAM_WEARABLE_PUPIL_DIAMETER,
    TOBII_CAPABILITY_COMPOUND_STREAM_WEARABLE_PUPIL_POSITION,
    TOBII_CAPABILITY_COMPOUND_STREAM_WEARABLE_EYE_OPENNESS,
    TOBII_CAPABILITY_COMPOUND_STREAM_WEARABLE_3D_GAZE_PER_EYE,
    TOBII_CAPABILITY_COMPOUND_STREAM_WEARABLE_USER_POSITION_GUIDE_XY,
    TOBII_CAPABILITY_COMPOUND_STREAM_WEARABLE_TRACKING_IMPROVEMENTS,
    TOBII_CAPABILITY_COMPOUND_STREAM_WEARABLE_CONVERGENCE_DISTANCE,
    TOBII_CAPABILITY_COMPOUND_STREAM_WEARABLE_IMPROVE_USER_POSITION_HMD,
    TOBII_CAPABILITY_COMPOUND_STREAM_WEARABLE_INCREASE_EYE_RELIEF,
} tobii_capability_t;

typedef enum tobii_supported_t
{
    TOBII_NOT_SUPPORTED,
    TOBII_SUPPORTED,
} tobii_supported_t;

typedef enum tobii_stream_t
{
    TOBII_STREAM_GAZE_POINT,
    TOBII_STREAM_GAZE_ORIGIN,
    TOBII_STREAM_EYE_POSITION_NORMALIZED,
    TOBII_STREAM_USER_PRESENCE,
    TOBII_STREAM_HEAD_POSE,
    TOBII_STREAM_WEARABLE,
    TOBII_STREAM_GAZE_DATA,
    TOBII_STREAM_DIGITAL_SYNCPORT,
    TOBII_STREAM_DIAGNOSTICS_IMAGE,
    TOBII_STREAM_CUSTOM,
} tobii_stream_t;

// typedefs for tobii_streams.h

typedef enum tobii_validity_t
{
    TOBII_VALIDITY_INVALID,
    TOBII_VALIDITY_VALID
} tobii_validity_t;

typedef struct tobii_gaze_point_t
{
    int64_t timestamp_us;

    tobii_validity_t validity;
    float position_xy[ 2 ];
} tobii_gaze_point_t;

typedef void (*tobii_gaze_point_callback_t)( tobii_gaze_point_t const* gaze_point, void* user_data );

typedef struct tobii_gaze_origin_t
{
    int64_t timestamp_us;

    tobii_validity_t left_validity;
    float left_xyz[ 3 ];

    tobii_validity_t right_validity;
    float right_xyz[ 3 ];
} tobii_gaze_origin_t;

typedef void (*tobii_gaze_origin_callback_t)( tobii_gaze_origin_t const* gaze_origin, void* user_data );

typedef struct tobii_eye_position_normalized_t
{
    int64_t timestamp_us;

    tobii_validity_t left_validity;
    float left_xyz[ 3 ];

    tobii_validity_t right_validity;
    float right_xyz[ 3 ];
} tobii_eye_position_normalized_t;

typedef void (*tobii_eye_position_normalized_callback_t)( tobii_eye_position_normalized_t const* eye_position, void* user_data );

typedef enum tobii_user_presence_status_t
{
    TOBII_USER_PRESENCE_STATUS_UNKNOWN,
    TOBII_USER_PRESENCE_STATUS_AWAY,
    TOBII_USER_PRESENCE_STATUS_PRESENT,
} tobii_user_presence_status_t;

typedef void (*tobii_user_presence_callback_t)( tobii_user_presence_status_t status, int64_t timestamp_us, void* user_data );

typedef struct tobii_head_pose_t
{
    int64_t timestamp_us;

    tobii_validity_t position_validity;
    float position_xyz[ 3 ];

    tobii_validity_t rotation_validity_xyz[ 3 ];
    float rotation_xyz[ 3 ];
} tobii_head_pose_t;

typedef void (*tobii_head_pose_callback_t)( tobii_head_pose_t const* head_pose, void* user_data );


// v-- this is not really described in the documentation
typedef struct tobii_display_area_t
{
    float top_left_mm_xyz[ 3 ];
    float top_right_mm_xyz[ 3 ];
    float bottom_left_mm_xyz[ 3 ];
} tobii_display_area_t;
// ^--


typedef enum tobii_enabled_eye_t
{
    TOBII_ENABLED_EYE_LEFT,
    TOBII_ENABLED_EYE_RIGHT,
    TOBII_ENABLED_EYE_BOTH,
} tobii_enabled_eye_t;

typedef enum tobii_notification_type_t
{
    TOBII_NOTIFICATION_TYPE_CALIBRATION_STATE_CHANGED,
    TOBII_NOTIFICATION_TYPE_EXCLUSIVE_MODE_STATE_CHANGED,
    TOBII_NOTIFICATION_TYPE_TRACK_BOX_CHANGED,
    TOBII_NOTIFICATION_TYPE_DISPLAY_AREA_CHANGED,
    TOBII_NOTIFICATION_TYPE_FRAMERATE_CHANGED,
    TOBII_NOTIFICATION_TYPE_POWER_SAVE_STATE_CHANGED,
    TOBII_NOTIFICATION_TYPE_DEVICE_PAUSED_STATE_CHANGED,
    TOBII_NOTIFICATION_TYPE_CALIBRATION_ENABLED_EYE_CHANGED,
    TOBII_NOTIFICATION_TYPE_CALIBRATION_ID_CHANGED,
    TOBII_NOTIFICATION_TYPE_COMBINED_GAZE_EYE_SELECTION_CHANGED,
    TOBII_NOTIFICATION_TYPE_FAULTS_CHANGED,
    TOBII_NOTIFICATION_TYPE_WARNINGS_CHANGED,
    TOBII_NOTIFICATION_TYPE_FACE_TYPE_CHANGED,
} tobii_notification_type_t;

typedef enum tobii_notification_value_type_t
{
    TOBII_NOTIFICATION_VALUE_TYPE_NONE,
    TOBII_NOTIFICATION_VALUE_TYPE_FLOAT,
    TOBII_NOTIFICATION_VALUE_TYPE_STATE,
    TOBII_NOTIFICATION_VALUE_TYPE_DISPLAY_AREA,
    TOBII_NOTIFICATION_VALUE_TYPE_UINT,
    TOBII_NOTIFICATION_VALUE_TYPE_ENABLED_EYE,
    TOBII_NOTIFICATION_VALUE_TYPE_STRING,
} tobii_notification_value_type_t;

typedef struct tobii_notification_t
{
    tobii_notification_type_t type;
    tobii_notification_value_type_t value_type;
    union
    {
        float float_;
        tobii_state_bool_t state;
        tobii_display_area_t display_area;
        uint32_t uint_;
        tobii_enabled_eye_t enabled_eye;
        tobii_state_string_t string_;
    } value;

} tobii_notification_t;

typedef void (*tobii_notifications_callback_t)( tobii_notification_t const* notification, void* user_data );

typedef struct tobii_user_position_guide_t
{
    int64_t timestamp_us;

    tobii_validity_t left_position_validity;
    float left_position_normalized_xyz[ 3 ];

    tobii_validity_t right_position_validity;
    float right_position_normalized_xyz[ 3 ];
} tobii_user_position_guide_t;

typedef void (*tobii_user_position_guide_callback_t)( tobii_user_position_guide_t const* user_position_guide, void* user_data );


// typedefs for tobii_wearable.h

typedef struct tobii_wearable_eye_t
{
    tobii_validity_t pupil_position_in_sensor_area_validity;
    float pupil_position_in_sensor_area_xy[ 2 ];

    tobii_validity_t position_guide_validity;
    float position_guide_xy[ 2 ];

    tobii_validity_t blink_validity;
    tobii_state_bool_t blink;
} tobii_wearable_eye_t;

typedef struct tobii_wearable_consumer_data_t
{
    int64_t timestamp_us;

    tobii_wearable_eye_t left;
    tobii_wearable_eye_t right;

    tobii_validity_t gaze_origin_combined_validity;
    float gaze_origin_combined_mm_xyz[ 3 ];

    tobii_validity_t gaze_direction_combined_validity;
    float gaze_direction_combined_normalized_xyz[ 3 ];

    tobii_validity_t convergence_distance_validity;
    float convergence_distance_mm;

    tobii_validity_t improve_user_position_hmd;
    tobii_state_bool_t increase_eye_relief;
} tobii_wearable_consumer_data_t;

typedef void (*tobii_wearable_consumer_data_callback_t)( tobii_wearable_consumer_data_t const* data, void* user_data );

typedef struct tobii_wearable_advanced_data_t
{
    int64_t timestamp_tracker_us;
    int64_t timestamp_system_us;

    tobii_wearable_eye_t left;
    tobii_wearable_eye_t right;

    tobii_validity_t gaze_origin_combined_validity;
    float gaze_origin_combined_mm_xyz[ 3 ];

    tobii_validity_t gaze_direction_combined_validity;
    float gaze_direction_combined_normalized_xyz[ 3 ];


    tobii_validity_t convergence_distance_validity;
    float convergence_distance_mm;

    tobii_validity_t improve_user_position_hmd;
    tobii_state_bool_t increase_eye_relief;
} tobii_wearable_advanced_data_t;

typedef void (*tobii_wearable_advanced_data_callback_t)( tobii_wearable_advanced_data_t const* data, void* user_data );

typedef struct tobii_lens_configuration_t
{
    float left_xyz[ 3 ];
    float right_xyz[ 3 ];
} tobii_lens_configuration_t;

typedef enum tobii_lens_configuration_writable_t
{
    TOBII_LENS_CONFIGURATION_NOT_WRITABLE,
    TOBII_LENS_CONFIGURATION_WRITABLE,
} tobii_lens_configuration_writable_t;

typedef enum tobii_wearable_foveated_tracking_state_t
{
    TOBII_WEARABLE_FOVEATED_TRACKING_STATE_TRACKING,
    TOBII_WEARABLE_FOVEATED_TRACKING_STATE_EXTRAPOLATED,
    TOBII_WEARABLE_FOVEATED_TRACKING_STATE_LAST_KNOWN,
} tobii_wearable_foveated_tracking_state_t;

typedef struct tobii_wearable_foveated_gaze_t
{
    int64_t timestamp_us;
    tobii_wearable_foveated_tracking_state_t tracking_state;
    float gaze_direction_combined_normalized_xyz[ 3 ];
} tobii_wearable_foveated_gaze_t;

typedef void (*tobii_wearable_foveated_gaze_callback_t)( tobii_wearable_foveated_gaze_t const* data, void* user_data );

// typedefs for tobii_licensing.h

typedef struct tobii_license_key_t
{
    uint16_t const* license_key;
    size_t size_in;
} tobii_license_key_t;

typedef enum tobii_license_validation_result_t
{
    TOBII_LICENSE_VALIDATION_RESULT_OK,
    TOBII_LICENSE_VALIDATION_RESULT_TAMPERED,
    TOBII_LICENSE_VALIDATION_RESULT_INVALID_APPLICATION_SIGNATURE,
    TOBII_LICENSE_VALIDATION_RESULT_NONSIGNED_APPLICATION,
    TOBII_LICENSE_VALIDATION_RESULT_EXPIRED,
    TOBII_LICENSE_VALIDATION_RESULT_PREMATURE,
    TOBII_LICENSE_VALIDATION_RESULT_INVALID_PROCESS_NAME,
    TOBII_LICENSE_VALIDATION_RESULT_INVALID_SERIAL_NUMBER,
    TOBII_LICENSE_VALIDATION_RESULT_INVALID_MODEL,
    TOBII_LICENSE_VALIDATION_RESULT_INVALID_PLATFORM_TYPE,
} tobii_license_validation_result_t;

typedef void (*tobii_data_receiver_t)( void const* data, size_t size, void* user_data );

typedef enum tobii_feature_group_t
{
    TOBII_FEATURE_GROUP_BLOCKED,
    TOBII_FEATURE_GROUP_CONSUMER,
    TOBII_FEATURE_GROUP_CONFIG,
    TOBII_FEATURE_GROUP_PROFESSIONAL,
    TOBII_FEATURE_GROUP_INTERNAL,
} tobii_feature_group_t;

// typedefs for tobii_config.h

// v-- this is not really described in the documentation
typedef enum tobii_calibration_point_status_t
{
    TOBII_CALIBRATION_POINT_STATUS_FAILED_OR_INVALID,
    TOBII_CALIBRATION_POINT_STATUS_VALID_BUT_NOT_USED_IN_CALIBRATION,
    TOBII_CALIBRATION_POINT_STATUS_VALID_AND_USED_IN_CALIBRATION,
} tobii_calibration_point_status_t;

typedef struct tobii_calibration_point_data_t
{
    float point_xy[ 2 ];

    tobii_calibration_point_status_t left_status;
    float left_mapping_xy[ 2 ];

    tobii_calibration_point_status_t right_status;
    float right_mapping_xy[ 2 ];
} tobii_calibration_point_data_t;
// ^--

typedef void (*tobii_calibration_point_data_receiver_t)( tobii_calibration_point_data_t const* point_data, void* user_data );

// v-- this is not really described in the documentation
typedef struct tobii_geometry_mounting_t
{
    int guides;
    float width_mm;
    float angle_deg;
    float external_offset_mm_xyz[ 3 ];
    float internal_offset_mm_xyz[ 3 ];
} tobii_geometry_mounting_t;
// ^--

typedef char tobii_device_name_t[ 64 ]; // this is not described in the documentation

typedef void (*tobii_output_frequency_receiver_t)( float output_frequency, void* user_data );

// typedefs for tobii_advanced.h

typedef struct tobii_gaze_data_eye_t
{
    tobii_validity_t gaze_origin_validity;
    float gaze_origin_from_eye_tracker_mm_xyz[ 3 ];
    float gaze_origin_in_track_box_normalized_xyz[ 3 ];

    tobii_validity_t gaze_point_validity;
    float gaze_point_from_eye_tracker_mm_xyz[ 3 ];
    float gaze_point_on_display_normalized_xy[ 2 ];

    tobii_validity_t eyeball_center_validity;
    float eyeball_center_from_eye_tracker_mm_xyz[ 3 ];

    tobii_validity_t pupil_validity;
    float pupil_diameter_mm;
} tobii_gaze_data_eye_t;

typedef struct tobii_gaze_data_t
{
    int64_t timestamp_tracker_us;
    int64_t timestamp_system_us;
    tobii_gaze_data_eye_t left;
    tobii_gaze_data_eye_t right;
} tobii_gaze_data_t;

typedef void (*tobii_gaze_data_callback_t)( tobii_gaze_data_t const* gaze_data, void* user_data );

typedef void (*tobii_digital_syncport_callback_t)( uint32_t signal, int64_t timestamp_tracker_us, int64_t timestamp_system_us, void* user_data );

typedef char tobii_face_type_t[ 64 ];

typedef void (*tobii_face_type_receiver_t)( const tobii_face_type_t face_type, void* user_data );
