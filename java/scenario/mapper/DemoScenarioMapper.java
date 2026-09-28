package com.ruoyi.scenario.mapper;

import java.util.List;
import java.util.Map;
import com.ruoyi.scenario.domain.DemoScenario;

/**
 * 云场景Mapper接口
 * 
 * @author ruoyi
 * @date 2026-06-23
 */
public interface DemoScenarioMapper 
{
    /**
     * 查询云场景
     * 
     * @param sceId 云场景主键
     * @return 云场景
     */
    public DemoScenario selectDemoScenarioBySceId(Long sceId);

    /**
     * 查询云场景列表
     * 
     * @param demoScenario 云场景
     * @return 云场景集合
     */
    public List<DemoScenario> selectDemoScenarioList(DemoScenario demoScenario);

    /**
     * 新增云场景
     * 
     * @param demoScenario 云场景
     * @return 结果
     */
    public int insertDemoScenario(DemoScenario demoScenario);

    /**
     * 修改云场景
     * 
     * @param demoScenario 云场景
     * @return 结果
     */
    public int updateDemoScenario(DemoScenario demoScenario);

    /**
     * 删除云场景
     * 
     * @param sceId 云场景主键
     * @return 结果
     */
    public int deleteDemoScenarioBySceId(Long sceId);

    /**
     * 批量删除云场景
     * 
     * @param sceIds 需要删除的数据主键集合
     * @return 结果
     */
    public int deleteDemoScenarioBySceIds(Long[] sceIds);

    /**
     * 审核云场景（批量更新状态）
     */
    public int updateScenarioByIds(Map<String, Object> params);


}
