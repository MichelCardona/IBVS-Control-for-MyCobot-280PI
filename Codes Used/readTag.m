function [coords, flag] = readTag(I, K, T_base_ee, tagSize, d)

    [id, ~, Rt] = readAprilTag(I, "tag36h11", K, tagSize);

    min_coord = [100, -150, 0];
    max_coord = [300, 150, 300];

    % R = Rt.A;

    if ~isempty(id) 

        flag = 1;

        T_cam_tag = Rt.A;
        T_ee_cam = eye(4);
        T_ee_cam(1,4) = 0.045;

        T_base_tag = T_base_ee * T_ee_cam * T_cam_tag;

        x = T_base_tag(1,4);
        y = T_base_tag(2,4);
        z = T_base_tag(3,4);

        R = T_base_tag(1:3,1:3);

        z_cam = R(:,3);
        goal = [x;y;z] - d*z_cam;

        x = goal(1)*1000;
        y = goal(2)*1000;
        z = goal(3)*1000;

        C_XYZ = [x,y,z];

        for i = 1:3
            if C_XYZ(i) < min_coord(i)
                C_XYZ(i) = min_coord(i);
            elseif C_XYZ(i) > max_coord(i)
                C_XYZ(i) = max_coord(i);
            end
        end

        eul = rotm2eul(R,"ZYX");

        rx = rad2deg(eul(3));
        ry = rad2deg(eul(2));
        rz = rad2deg(eul(1));

        coords = [C_XYZ,rx,ry,rz];
    else 
        flag = 0;
        coords = [0 0 0 0 0 0];
    end


end