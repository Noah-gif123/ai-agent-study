package com.ruoyi.scenario.controller;

import java.util.List;

import com.ruoyi.common.core.page.TableDataInfo;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import com.ruoyi.common.annotation.Anonymous;
import com.ruoyi.common.core.controller.BaseController;
import com.ruoyi.common.core.domain.AjaxResult;
import com.ruoyi.scenario.domain.DemoScenario;
import com.ruoyi.scenario.service.IDemoScenarioService;
import com.ruoyi.web.controller.common.Const;
import com.ruoyi.common.core.redis.RedisCache;

/**
 * 云场景前端API Controller
 *
 * @author ruoyi
 * @date 2026-06-24
 */
@Anonymous
@RestController
@RequestMapping("/api/scenario")
public class DemoScenarioApiController extends BaseController {

    @Autowired
    private IDemoScenarioService demoScenarioService;

    @Autowired
    private RedisCache redisCache;

    /**
     * 获取云场景列表（匿名访问）
     */
    @GetMapping("/list")
    public TableDataInfo list(DemoScenario demoScenario) {
        demoScenario.setSceStatus(Const.SCE_STATUS_OPEN);
        startPage();
        List<DemoScenario> list = demoScenarioService.selectDemoScenarioList(demoScenario);
        if(list!=null) {
            for(DemoScenario ds:list) {
                Long reads = redisCache.getCacheObject(Const.SCENARIO_READS + ds.getSceId());
                if (reads != null) {
                    ds.setSceReads(reads);
                }
            }
        }
        return getDataTable(list);
    }

    /**
     * 获取云场景详情（匿名访问）
     */
    @GetMapping(value = "/{id}")
    public AjaxResult getInfo(@PathVariable("id") Long id)
    {
        DemoScenario demoScenario = demoScenarioService.selectDemoScenarioBySceId(id);
        Long reads = redisCache.getCacheObject(Const.SCENARIO_READS+id);
        if(reads==null){
            reads = demoScenario.getSceReads();
        }
        redisCache.setCacheObject(Const.SCENARIO_READS+id, reads+1);
        demoScenario.setSceReads(reads+1);
        return AjaxResult.success(demoScenario);
    }
}
