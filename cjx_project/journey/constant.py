from .forms import Touchpoint_Form, Journey_Customer_Form, Action_Type_Form, Channel_Type_Form, Source_Type_Form, Device_Browser_Form, Device_OS_Form, Device_Category_Form, Interact_Item_Type_Form, Experience_Emotion_Form, Matching_Report_Form, Matching_Column_Form

formData = {
    'touchpoint'            : Touchpoint_Form,
    'journey_customer'      : Journey_Customer_Form,
    'action_type'           : Action_Type_Form,
    'channel_type'          : Channel_Type_Form,
    'traffic_source_type'   : Source_Type_Form,
    'device_browser'        : Device_Browser_Form,
    'device_os'             : Device_OS_Form,
    'device_category'       : Device_Category_Form,
    'interact_item_type'    : Interact_Item_Type_Form,
    'experience_emotion'    : Experience_Emotion_Form,
    'matching_column'       : Matching_Column_Form,
    'matching_report'       : Matching_Report_Form
}

functions = ['lower', 'upper', 'string', 'int', 'float', 'datetime', 'date']

documentation_pages = [
        {
            'name'              : 'quick-start',
            'icon'              : '/static/journey/images/i-docs_quickstart.svg',
            'href'              : '/journey/documentation/quick-start',
            'title'             : 'Quickstart',
            'content'           : 'Learn everything about Customer Journey Master and get started right now',
            'html_file'         : 'journey/documentation-quickstart.html',
            'previous_content'  : 'API Integration',
            'previous_href'     : '/journey/documentation/api-integration',
            'next_content'      : 'Data Model',
            'next_href'         : '/journey/documentation/data-model'
        }, 
        {
            'name'              : 'data-model',
            'icon'              : '/static/journey/images/i-docs_environment.svg',
            'href'              : '/journey/documentation/data-model',
            'title'             : 'Data Model',
            'content'           : 'Find out Main Data Models of Customer Journey and their fields',
            'html_file'         : 'journey/documentation-datamodel.html',
            'previous_content'  : 'Quick Start',
            'previous_href'     : '/journey/documentation/quick-start',
            'next_content'      : 'Import',
            'next_href'         : '/journey/documentation/import'
        }, 
        {
            'name'              : 'import',
            'icon'              : '/static/journey/images/i-docs_tracking.svg',
            'href'              : '/journey/documentation/import',
            'title'             : 'Import',
            'content'           : 'Find out how to manually add, update, delete data into tables',
            'html_file'         : 'journey/documentation-import.html',
            'previous_content'  : 'Data Model',
            'previous_href'     : '/journey/documentation/data-model',
            'next_content'      : 'Process Analytics',
            'next_href'         : '/journey/documentation/process-analytics'
        }, 
        {
            'name'              : 'process-analytics',
            'icon'              : '/static/journey/images/i-docs_predictive.svg',
            'href'              : '/journey/documentation/process-analytics',
            'title'             : 'Process Analytics',
            'content'           : 'Use our machine learning algorithms: process mining, clustering and decision tree to analyze user behavior',
            'html_file'         : 'journey/documentation-process-analytics.html',
            'previous_content'  : 'Import',
            'previous_href'     : '/journey/documentation/import',
            'next_content'      : 'Report',
            'next_href'         : '/journey/documentation/reports'
        }, 
        {
            'name'              : 'reports',
            'icon'              : '/static/journey/images/i-docs_reports.svg',
            'href'              : '/journey/documentation/reports',
            'title'             : 'Report',
            'content'           : 'Build reports on a wide range of metrics and data types',
            'html_file'         : 'journey/documentation-reports.html',
            'previous_content'  : 'Process Analytics',
            'previous_href'     : '/journey/documentation/process-analytics',
            'next_content'      : 'API Integration',
            'next_href'         : '/journey/documentation/api-integration'
        }, 
        {
            'name'              : 'api-integration',
            'icon'              : '/static/journey/images/i-docs_api.svg',
            'href'              : '/journey/documentation/api-integration',
            'title'             : 'API Integration',
            'content'           : 'Integrate tracked data from multi-platforms: e-commerce website, mobile application, ... by API',
            'html_file'         : 'journey/documentation-api-integration.html',
            'previous_content'  : 'Report',
            'previous_href'     : '/journey/documentation/reports',
            'next_content'      : 'Quick Start',
            'next_href'         : '/journey/documentation/quick-start'
        }
    ]

