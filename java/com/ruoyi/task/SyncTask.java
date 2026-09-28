package com.ruoyi.task;
import java.util.List;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import com.ruoyi.common.core.redis.RedisCache;
import com.ruoyi.scenario.domain.DemoScenario;
import com.ruoyi.scenario.service.IDemoScenarioService;
import com.ruoyi.web.controller.common.Const;
import com.ruoyi.web.controller.common.SpringUtil;
@Component
public class SyncTask {
    private static final Logger log = LoggerFactory.getLogger(SyncTask.class);
    @Autowired
    private RedisCache redisCache;
    @Autowired
    private IDemoScenarioService demoScenarioService;

    public void redis2DB() {
        new Thread(() -> {
            // 云场景浏览量同步数据库
            DemoScenario demoScenario = new DemoScenario();
            demoScenario.setSceStatus(Const.SCE_STATUS_OPEN);
            demoScenarioService = SpringUtil.getBean(IDemoScenarioService.class);
            List<DemoScenario> demoScenarioList = demoScenarioService.selectDemoScenarioList(demoScenario);
            redisCache = SpringUtil.getBean(RedisCache.class);
            for (DemoScenario s : demoScenarioList) {
                try {
                    Long readNum = redisCache.getCacheObject(Const.SCENARIO_READS + s.getSceId());
                    if (readNum != null) {
                        DemoScenario ds = new DemoScenario();
                        ds.setSceId(s.getSceId());
                        ds.setSceReads(readNum);
                        demoScenarioService.updateDemoScenario(ds);
                    }
                } catch (Exception e) {
                    log.error("云场景Redis同步数据库出错,当前场景ID：'{}'", s.getSceId());
                }
            }
        }).start();
    }
}