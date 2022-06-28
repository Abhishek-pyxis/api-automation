class ApiResources:
    # GET APIs
    read_fake_story = "fake_stories/{context.story_id}"
    get_rows_by_story_ai_model = "ai_model_stories/{context.story_id}"
    read_schedule_by_story = "optimization_schedules/1000000"
    read_phases_by_fb_id = "phases/{context.ad_account_id}"
    read_rows_by_story_id_keywords_settings = 'keywords_settings/{context.story_id}'
    read_rows_by_story_id_keywords_metrics = "keywords_metrics/{context.story_id}"
    read_rows_by_story_id_keywords_delta_items = "keywords_delta_items/{context.story_id}"

    # POST APIs
    create_fake_story = "fake_stories/"
    set_rows_by_story_ai_model = "ai_model_stories/{context.story_id}"
    set_optimization_schedules = "optimization_schedules/?frequency_launch={context.frequency_launch}&start_time={" \
                                 "context.start_time} "
    create_trigger_by_story = "optimization_schedules/1000000"
    set_phases_by_fb_id = "phases/?fb_id={context.ad_account_id}"
    set_rows_by_story_id_keywords_settings = "keywords_settings/{context.story_id}"
    set_rows_by_story_id_keywords_metrics = "keywords_metrics/{context.story_id}"
    set_rows_by_story_id_keywords_delta_items = "keywords_delta_items/{context.story_id}"

    # PUT APIs
    update_fake_story = "fake_stories/{context.story_id}"
    update_phase = "phases/{context.ad_account_id}?phase_id={context.phase_id}"

    # DELETE APIs
    delete_story = "fake_stories/{context.story_id}"
    delete_schedule_by_story = "optimization_schedules/1000000"
    delete_phase = "phases/{context.ad_account_id}?phase_id={context.phase_id}"
    delete_rows_by_story_id_keywords_settings = "keywords_settings/{context.story_id}"
    delete_rows_by_story_id_keywords_metrics = "keywords_metrics/{context.story_id}"
    delete_rows_by_story_id_keywords_delta_items = "keywords_delta_items/{context.story_id}"
