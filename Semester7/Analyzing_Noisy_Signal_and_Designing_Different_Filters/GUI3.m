function audio_filter_gui
    % Create GUI Figure
    fig = uifigure('Name', 'Audio Filter GUI', 'Position', [100, 100, 1280, 720]);

    % Axes for Signal Visualization
    ax1 = uiaxes(fig, 'Position', [50, 340, 550, 245]);
    title(ax1, 'Original Signal');
    xlabel(ax1, 'Time (s)');
    ylabel(ax1, 'Amplitude');

    ax2 = uiaxes(fig, 'Position', [650, 340, 550, 245]);
    title(ax2, 'Filtered Signal');
    xlabel(ax2, 'Time (s)');
    ylabel(ax2, 'Amplitude');

    axFFT1 = uiaxes(fig, 'Position', [50, 50, 550, 245]);
    title(axFFT1, 'Original Signal - Frequency Domain');
    xlabel(axFFT1, 'Frequency (Hz)');
    ylabel(axFFT1, 'Magnitude');

    axFFT2 = uiaxes(fig, 'Position', [650, 50, 550, 245]);
    title(axFFT2, 'Frequency Response of the Filter');
    xlabel(axFFT2, 'Frequency (Hz)');
    ylabel(axFFT2, 'Magnitude');

    % Button to Load Audio File
    btnLoad = uibutton(fig, 'Text', 'Load Audio', 'Position', [50, 670, 100, 30], ...
                       'Tooltip', 'Click to load an audio file.');
    btnLoad.ButtonPushedFcn = @(~, ~) loadAudio();

    % Dropdown for Filter Selection
    lblFilter = uilabel(fig, 'Text', 'Filter Type:', 'Position', [200, 670, 80, 20], ...
                        'FontSize', 12, 'FontWeight', 'bold');
    dropdownFilter = uidropdown(fig, 'Items', {'Lowpass', 'Highpass', 'Bandpass', 'Bandstop', 'No Filter', 'Moving Average'}, ...
                                'Position', [280, 670, 100, 30], 'ValueChangedFcn', @(~, ~) toggleSliders());

    % Slider for Cutoff Frequency
    lblCutoff = uilabel(fig, 'Text', 'Cutoff Freq (Hz):', 'Position', [400, 670, 100, 20], ...
                        'Tooltip', 'Adjust the cutoff frequency for Lowpass or Highpass filters.');
    sliderCutoff = uislider(fig, 'Position', [510, 675, 150, 3], 'Limits', [50, 10000]);
    lblCutoffValue = uilabel(fig, 'Text', 'Value: 1000 Hz', 'Position', [550, 690, 100, 20]);

    % Slider for Bandpass / Bandstop Frequencies
    lblHighFreq = uilabel(fig, 'Text', 'High Freq (Hz):', 'Position', [700, 670, 100, 20], ...
                          'Tooltip', 'Set the high frequency for Bandpass or Bandstop filters.');
    sliderHighFreq = uislider(fig, 'Position', [810, 675, 150, 3], 'Limits', [50, 10000], 'Enable', 'off');
    lblHighFreqValue = uilabel(fig, 'Text', 'Value: 100 Hz', 'Position', [850, 690, 100, 20]);

    lblLowFreq = uilabel(fig, 'Text', 'Low Freq (Hz):', 'Position', [700, 610, 100, 20], ...
                         'Tooltip', 'Set the low frequency for Bandpass or Bandstop filters.');
    sliderLowFreq = uislider(fig, 'Position', [810, 610, 150, 3], 'Limits', [50, 10000], 'Enable', 'off');
    lblLowFreqValue = uilabel(fig, 'Text', 'Value: 500 Hz', 'Position', [850, 620, 100, 20]);

    % Slider for Moving Average Window Size 
    lblMovAvgWindow = uilabel(fig, 'Text', 'Window Size:', 'Position', [50, 630, 100, 20], ...
                              'Tooltip', 'Set the window size for Moving Average filter.');
    sliderMovAvg = uislider(fig, 'Position', [160, 630, 150, 3], 'Limits', [1, 1000], 'Enable', 'off');
    lblMovAvgValue = uilabel(fig, 'Text', 'Value: 100', 'Position', [200, 645, 100, 20]);

    % Button to Apply Filter
    btnFilter = uibutton(fig, 'Text', 'Apply Filter', 'Position', [1100, 660, 100, 30], ...
                         'Tooltip', 'Click to apply the selected filter.');
    btnFilter.ButtonPushedFcn = @(~, ~) applyFilter();

    % Play/Pause Button
    btnPlayPause = uibutton(fig, 'Text', 'Play', 'Position', [1100, 610, 100, 30], ...
                            'Tooltip', 'Click to play/pause the audio.');
    btnPlayPause.ButtonPushedFcn = @(~, ~) playPauseAudio();

    % Slider to Adjust Sampling Rate 
    lblSampleRate = uilabel(fig, 'Text', 'Sample Rate (Hz):', 'Position', [400, 610, 120, 20]);
    sliderSampleRate = uislider(fig, 'Position', [510, 615, 150, 3], 'Limits', [8000, 96000], 'Value', 44100);
    lblSampleRateValue = uilabel(fig, 'Text', '44100 Hz', 'Position', [560, 625, 100, 20]);

    % Variables to Store Audio Data
    audioData = [];
    originalAudioData = [];
    sampleRate = 44100;
    filteredAudio = [];
    isPlaying = false;
    player = [];

    % Callback: Load Audio File
    function loadAudio()
        [file, path] = uigetfile({'*.mp3;*.wav', 'Audio Files (*.mp3, *.wav)'}); 
        if isequal(file, 0)
            return;
        end
        [audioData, sampleRate] = audioread(fullfile(path, file));
        originalAudioData = audioData; % Store original data for playback
        if size(audioData, 2) > 1
            audioData = audioData(:, 1); % Process only the first channel
        end
        time = (0:length(audioData)-1) / sampleRate;
        plot(ax1, time, audioData);
        title(ax1, sprintf('Original Signal (Sample Rate: %d Hz)', sampleRate));
        xlabel(ax1, 'Time (s)');
        ylabel(ax1, 'Amplitude');
        filteredAudio = audioData;
        plotFFT(axFFT1, audioData, sampleRate);
    end

function applyFilter()
    if isempty(audioData)
        uialert(fig, 'Please load an audio file first.', 'Error');
        return;
    end

    % Get Filter Type and Parameters
    filterType = dropdownFilter.Value;
    cutoffFreq = sliderCutoff.Value;
    windowSize = sliderMovAvg.Value;

    try
        switch filterType
            case 'Lowpass'
                [b, a] = butter(4, cutoffFreq / (sampleRate / 2), 'low');
            case 'Highpass'
                [b, a] = butter(4, cutoffFreq / (sampleRate / 2), 'high');
            case 'Bandpass'
                lowFreq = sliderLowFreq.Value;
                highFreq = sliderHighFreq.Value;
                if lowFreq >= highFreq
                    uialert(fig, 'Low frequency must be less than high frequency.', 'Error');
                    return;
                end
                [b, a] = butter(4, [lowFreq, highFreq] / (sampleRate / 2), 'bandpass');
            case 'Bandstop'
                lowFreq = sliderLowFreq.Value;
                highFreq = sliderHighFreq.Value;
                if lowFreq >= highFreq
                    uialert(fig, 'Low frequency must be less than high frequency.', 'Error');
                    return;
                end
                [b, a] = butter(4, [lowFreq, highFreq] / (sampleRate / 2), 'stop');
            case 'No Filter'
                filteredAudio = audioData; % No filtering applied, just use the original signal
                plot(ax2, (0:length(filteredAudio)-1) / sampleRate, filteredAudio); % Plot the original signal
                % Plot frequency response for No Filter (same as original signal)
                plotFFT(axFFT2, filteredAudio, sampleRate); 
                return;
            case 'Moving Average'
                filteredAudio = movmean(audioData, windowSize); % Apply moving average filter
                plot(ax2, (0:length(filteredAudio)-1) / sampleRate, filteredAudio); % Plot filtered signal
                % Plot frequency response for Moving Average filter
                plotFFT(axFFT2, filteredAudio, sampleRate);
                return;
            otherwise
                error('Unknown filter type');
        end

        % Apply Butterworth Filter and Plot Frequency Response
        filteredAudio = filter(b, a, audioData);
        plot(ax2, (0:length(filteredAudio)-1) / sampleRate, filteredAudio); % Plot filtered signal
        plotFrequencyResponse(axFFT2, b, a, sampleRate); % Plot frequency response

    catch
        uialert(fig, 'An error occurred while applying the filter.', 'Error');
    end
end




    % Function to Plot FFT
    function plotFFT(ax, data, fs)
        n = length(data);
        f = (0:n-1) * (fs / n);
        mag = abs(fft(data));
        plot(ax, f(1:n/2), mag(1:n/2));
        title(ax, 'Frequency Domain');
        xlabel(ax, 'Frequency (Hz)');
        ylabel(ax, 'Magnitude');
    end

    % Function to Plot Frequency Response
    function plotFrequencyResponse(ax, b, a, fs)
        [h, f] = freqz(b, a, 1024, fs); % Frequency response of the filter
        plot(ax, f, abs(h)); % Plot magnitude response
        title(ax, 'Frequency Response of the Filter');
        xlabel(ax, 'Frequency (Hz)');
        ylabel(ax, 'Magnitude');
    end

    % Callback: Toggle Sliders Based on Filter Type
    function toggleSliders()
        filterType = dropdownFilter.Value;
        switch filterType
            case {'Bandpass', 'Bandstop'}
                sliderLowFreq.Enable = 'on';
                sliderHighFreq.Enable = 'on';
            case 'Moving Average'
                sliderMovAvg.Enable = 'on';
                sliderCutoff.Enable = 'off';
            otherwise
                sliderLowFreq.Enable = 'off';
                sliderHighFreq.Enable = 'off';
                sliderMovAvg.Enable = 'off';
                sliderCutoff.Enable = 'on';
        end
    end

    % Callback: Play/Pause Audio
    function playPauseAudio()
        if isempty(filteredAudio)
            return;
        end
        if isPlaying
            pause(player);
            btnPlayPause.Text = 'Play';
        else
            player = audioplayer(filteredAudio, sampleRate);
            play(player);
            btnPlayPause.Text = 'Pause';
        end
        isPlaying = ~isPlaying;
    end
end
