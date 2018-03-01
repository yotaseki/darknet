data1 = csvread('180218_robocup2017_255predict_ball_PRcurve.csv');
data2 = csvread('180218_robocup2017_3982predict_ball_PRcurve.csv');
data3 = csvread('180218_shinnara_3727predict_ball_PRcurve.csv');
data1 = data1';
data2 = data2';
data3 = data3';
figure;
plot(data1(1,:),data1(2,:),data2(1,:),data2(2,:),data3(1,:),data3(2,:),'LineWidth',4);
title('Ball-class Precision-Recall curve','FontSize',20)
ylabel('Recall','FontSize',16);
xlabel('Precision','FontSize',16);
legend({'(A)255images','(B)3727images','(C)3982images'}, 'FontSize',12,'Location','southwest')
%xlim([0 1]);
%ylim([0 1]);
saveas(gcf,'out.png')
