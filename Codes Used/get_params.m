function Params = get_params()
    data = load("cameraParams.mat");
    Params = data.cameraParams.Intrinsics;
    % K = Params.K;
    % Radial = Params.RadialDistortion;
    % Tang = Params.TangentialDistortion;
    % Skew = Params.Skew;
    % dist = [Radial, Tang, Skew];
end